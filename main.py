# main.py

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"   # Hide TensorFlow warnings

import pandas as pd

from config import KEYWORDS
from ingestion.google_search import fetch_google_results
from processing.text_cleaning import clean_text
from processing.sentiment import sentiment_score
from processing.brand_detection import detect_brand
from analytics.sov_metrics import compute_sov, compute_sov_by_keyword
from analytics.insights import generate_insights


def run_pipeline():
    all_rows = []

    # ---------------------------------------------------------
    # Fetch Google results for each keyword
    # ---------------------------------------------------------
    for kw in KEYWORDS:
        print(f"\n=== Keyword: {kw} ===")
        rows = fetch_google_results(kw)
        print(f"Google results: {len(rows)}")
        all_rows.extend(rows)

    if not all_rows:
        raise RuntimeError("No data fetched from Google. Check SERPAPI_KEY / quota.")

    df = pd.DataFrame(all_rows)

    # ---------------------------------------------------------
    # Build combined text field (title + snippet)
    # ---------------------------------------------------------
    df["text"] = df["title"].fillna("") + " " + df["snippet"].fillna("")

    print("Cleaning text...")
    df["clean_text"] = df["text"].apply(clean_text)

    # ---------------------------------------------------------
    # Sentiment analysis FIRST (required for brand detection)
    # ---------------------------------------------------------
    print("Running sentiment analysis...")
    df["sentiment"] = df["clean_text"].apply(sentiment_score)

    # ---------------------------------------------------------
    # Brand detection (lexical + fuzzy + category + semantic)
    # ---------------------------------------------------------
    print("Detecting brands...")
    df["brand"] = df.apply(
        lambda row: detect_brand(row["clean_text"], row["sentiment"]),
        axis=1
    )

    # ---------------------------------------------------------
    # Compute SOV metrics
    # ---------------------------------------------------------
    print("Computing SOV metrics...")
    sov_global = compute_sov(df)
    sov_kw = compute_sov_by_keyword(df)

    # ---------------------------------------------------------
    # Save output files
    # ---------------------------------------------------------
    df.to_csv("data/raw_google_results.csv", index=False)
    sov_global.to_csv("data/sov_summary_global.csv", index=False)
    sov_kw.to_csv("data/sov_summary_by_keyword.csv", index=False)

    print("\n=== Global SOV Summary ===")
    print(sov_global)

    # ---------------------------------------------------------
    # Generate insights (Markdown)
    # ---------------------------------------------------------
    print("\nGenerating insights...")
    insights_md = generate_insights(df, sov_global, sov_kw)

    with open("data/insights.md", "w", encoding="utf-8") as f:
        f.write(insights_md)

    print("\nInsights saved to data/insights.md")
    print("Pipeline complete.")


if __name__ == "__main__":
    run_pipeline()
