# processing/brand_detection.py

import re
from functools import lru_cache
from typing import Optional, Dict

import torch
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer, util

from config import (
    BRAND_ALIASES,
    BRAND_DESCRIPTIONS,
    CATEGORY_TRIGGERS,
    ATOMBERG_PRIORITY_BOOST,
    ATOMBERG_FUZZY_THRESHOLD,
)


# -----------------------------------------------------------
# TEXT NORMALIZATION
# -----------------------------------------------------------
def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -----------------------------------------------------------
# LOAD SEMANTIC MODEL (CACHED)
# -----------------------------------------------------------
@lru_cache(maxsize=1)
def get_semantic_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# -----------------------------------------------------------
# PRECOMPUTE BRAND EMBEDDINGS
# -----------------------------------------------------------
@lru_cache(maxsize=1)
def get_brand_embeddings() -> Dict[str, torch.Tensor]:
    model = get_semantic_model()

    full_texts = []
    brand_names = []

    for brand, desc in BRAND_DESCRIPTIONS.items():
        alias_text = " ".join(BRAND_ALIASES.get(brand, []))
        combined = f"{brand}. {desc}. {alias_text}"
        full_texts.append(combined)
        brand_names.append(brand)

    embeddings = model.encode(
        full_texts, convert_to_tensor=True, normalize_embeddings=True
    )

    return {b: emb for b, emb in zip(brand_names, embeddings)}


# -----------------------------------------------------------
# MAIN DETECTION LOGIC
# -----------------------------------------------------------
def detect_brand(text: str, sentiment: float = 0.0) -> Optional[str]:
    """
    Brand Detection Workflow:
    1. Exact alias match
    2. Fuzzy alias match (Atomberg more flexible)
    3. Category triggers (BLDC, energy saving → Atomberg)
    4. Negative competitor override (skip assigning competitor)
    5. Semantic similarity (MiniLM) with Atomberg boost
    """

    if not text:
        return None

    norm = _normalize(text)

    # VERY negative sentiment => do NOT assign competitor
    avoid_competitor = sentiment < -0.45

    # ----------------------------
    # 1. EXACT / ALIAS MATCH
    # ----------------------------
    for brand, aliases in BRAND_ALIASES.items():
        for alias in aliases:
            alias_norm = _normalize(alias)
            pattern = rf"\b{re.escape(alias_norm)}\b"
            if re.search(pattern, norm):
                if not avoid_competitor:
                    return brand

    # ----------------------------
    # 2. FUZZY MATCH (typos allowed)
    # ----------------------------
    for brand, aliases in BRAND_ALIASES.items():

        threshold = ATOMBERG_FUZZY_THRESHOLD if brand == "Atomberg" else 85

        for alias in aliases:
            if fuzz.partial_ratio(alias.lower(), norm) > threshold:
                if not avoid_competitor:
                    return brand

    # ----------------------------
    # 3. CATEGORY TRIGGERS
    # (BLDC / energy saving → Atomberg)
    # ----------------------------
    for trig in CATEGORY_TRIGGERS:
        if trig in norm:
            if not avoid_competitor:
                return "Atomberg"

    # ----------------------------
    # 4. SEMANTIC SIMILARITY
    # ----------------------------
    semantic_model = get_semantic_model()
    brand_embs = get_brand_embeddings()

    text_emb = semantic_model.encode(
        norm, convert_to_tensor=True, normalize_embeddings=True
    )

    best_brand = None
    best_score = 0.0

    for brand, emb in brand_embs.items():
        sim = float(util.cos_sim(text_emb, emb)[0][0])

        # Boost Atomberg similarity score
        if brand == "Atomberg":
            sim *= ATOMBERG_PRIORITY_BOOST

        if sim > best_score:
            best_score = sim
            best_brand = brand

    # semantic threshold
    SEMANTIC_THRESHOLD = 0.30

    if best_score >= SEMANTIC_THRESHOLD:
        return best_brand

    return None
