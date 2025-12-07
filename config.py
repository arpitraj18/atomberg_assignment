# config.py
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

# API key
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Search settings
TOP_N = int(os.getenv("TOP_N", 20))
KEYWORDS = [k.strip() for k in os.getenv(
    "KEYWORDS",
    "smart fan,bldc fan,energy saving fan"
).split(",") if k.strip()]

# Brand aliases & descriptions for semantic detection
BRAND_ALIASES = {
"Atomberg": [
"atomberg",
"atom berg",
"atomberg fan",
"atomberg fans",
"atomberg bldc",
"atomberg bldc fan",
"atomberg bldc fans",
"atomberg renesa",
"renesa",
"renesa smart fan",
"renesa ceiling fan",
"atomberg studio",
"studio atomberg",
"gorilla fan",
"gorilla fans",
"gorilla ceiling fan",
"gorilla bldc fan",
"gorilla renesa",
"bldc fan atomberg",
"bldc atomberg",
"renesa bldc",
"renesa bldc fan",
"energy saving atomberg",
"energy efficient atomberg",
"atomberg smart fan",
"smart fan atomberg",
"smart bldc atomberg",
],
"Havells": [
        "havells",
        "havells smart fan",
    ],
    "Crompton": [
        "crompton",
        "crompton smart fan",
        "crompton greaves",
    ],
    "Orient": [
        "orient",
        "orient electric",
    ],
    "Bajaj": [
        "bajaj",
        "bajaj fan",
    ],
    "Usha": [
        "usha",
        "usha fan",
    ],
}

BRAND_DESCRIPTIONS = {
    "Atomberg": "Atomberg BLDC smart energy saving ceiling fans, Gorilla fans brand",
    "Havells": "Havells ceiling fans and smart fans brand in India",
    "Crompton": "Crompton Greaves ceiling fans and smart fans",
    "Orient": "Orient Electric ceiling fans and smart fans brand",
    "Bajaj": "Bajaj ceiling fans and home appliances brand",
    "Usha": "Usha ceiling fans and home appliances brand",
}

BRANDS = list(BRAND_ALIASES.keys())

# Keywords that indicate the discussion is about the BLDC / energy-saving category
# used for simple category-trigger based brand assignment (Atomberg dominates this
# category in our dataset).
CATEGORY_TRIGGERS = [
    "bldc",
    "bldc fan",
    "energy saving",
    "energy-saving",
    "energy efficient",
    "energy efficient fan",
    "smart fan",
]

# Extra triggers to increase Atomberg recall
CATEGORY_TRIGGERS += [
    "bldc motor",
    "bldc ceiling fan",
    "bldc technology",
    "dc motor",
    "dc fan",
    "dc ceiling fan",
    "energy saving ceiling fan",
    "energy efficient ceiling fan",
    "inverter fan",
    "low energy fan",
]

# Atomberg-specific tuning: boost semantic score and lower fuzzy threshold
ATOMBERG_PRIORITY_BOOST = float(os.getenv("ATOMBERG_PRIORITY_BOOST", 1.2))
ATOMBERG_FUZZY_THRESHOLD = int(os.getenv("ATOMBERG_FUZZY_THRESHOLD", 80))
