# 🔎 Atomberg Smart Fan Share-of-Voice (SoV) Intelligence Platform
### **AI-Powered Competitive Intelligence for India’s BLDC & Smart Fan Market**

An enterprise-grade **Share-of-Voice Intelligence Platform** designed to monitor, analyze, and optimize **Atomberg’s brand visibility, sentiment, and competitive positioning** across high-intent Google search queries in the Indian smart fan market.

Built using **Artificial Intelligence, Natural Language Processing (NLP), and Semantic Search**, this system transforms raw Google search results into **actionable marketing and growth intelligence**.

---

## 🎯 Executive Overview

This platform continuously tracks how **Atomberg and competing brands** (Havells, Crompton, Orient, Bajaj, Usha) perform across critical consumer search journeys such as:

* “Smart fan”
* “BLDC fan”
* “Energy saving ceiling fan”

It delivers:

* ✅ Real-time **brand visibility dominance**
* ✅ **Sentiment-weighted competitive positioning**
* ✅ **Keyword-level opportunity detection**
* ✅ **Automated strategic marketing recommendations**

---

## 📌 Key Business Outcomes

For Atomberg’s **Marketing, Growth & Product Strategy teams**, this system enables:

* Measure **true digital market share**, not just mentions
* Identify **high-converting keyword battlegrounds**
* Detect **sentiment risks & reputation gaps**
* Discover **brand messaging weaknesses vs competitors**
* Track **SEO & content performance against rivals**
* Support **media planning & digital ad targeting decisions**

---

## 🚀 Platform Capabilities

### 1. High-Fidelity Google Intelligence Engine
Powered by **SerpAPI**, the platform ingests:
* Search result title
* Snippet context
* Page URL
* Exact Google ranking position
* Multi-keyword market coverage

### 2. AI-Driven Brand Recognition Engine
A **three-layer hybrid detection framework** ensures enterprise-grade accuracy:
1. Exact brand alias recognition
2. Fuzzy brand matching (RapidFuzz)
3. Semantic brand similarity (MiniLM embeddings)

Detects **implicit, indirect, and noisy brand references** with extremely high precision.

### 3. Consumer Sentiment Intelligence
Uses **DistilBERT NLP models**, enhanced with domain-specific triggers:
* Negative sentiment cues: noisy, high power consumption, durability issue
* Positive sentiment cues: energy saving, silent operation, smart control

Delivers **true consumer perception modeling** instead of generic polarity scoring.

### 4. Executive-Grade Share-of-Voice Metrics
**For each brand:**
* Volume SoV — pure mention share
* Visibility SoV — rank-weighted digital dominance
* Positive Voice SoV — sentiment-adjusted brand strength

**For each keyword:**
* Market share distribution
* Competitive intensity mapping
* Keyword ownership scoring

### 5. Automated Strategic Intelligence Engine
Generates executive-ready insights including:
* Market leaders & challengers
* Brand-wise sentiment summaries
* High-opportunity keyword clusters
* Competitive messaging gaps
* Performance-driven growth recommendations

Exported as:
`data/insights.md`

### 6. Interactive Strategy Dashboard (Streamlit)
Leadership-friendly real-time analytics including:
* Global SoV share visualization
* Keyword-level competitive heatmaps
* Brand dominance breakdown
* Raw Google intelligence explorer
* AI-generated insights viewer
* Dynamic decision filters

---

## 🧩 System Architecture

```text
smart_fan_sov/
│
├── config.py
├── main.py
├── requirements.txt
├── .env.example
│
├── data/
│   ├── raw_google_results.csv
│   ├── sov_summary_global.csv
│   ├── sov_summary_by_keyword.csv
│   └── insights.md
│
├── ingestion/
│   └── google_search.py
│
├── processing/
│   ├── text_cleaning.py
│   ├── brand_detection.py
│   └── sentiment.py
│
├── analytics/
│   ├── sov_metrics.py
│   └── insights.py
│
└── dashboard/
    └── app.py
```

---

## ⚙️ Deployment & Execution

### 1️⃣ Secure Setup
```bash
git clone [https://github.com/YOUR_USERNAME/smart_fan_sov.git](https://github.com/YOUR_USERNAME/smart_fan_sov.git)
cd smart_fan_sov
pip install -r requirements.txt
```

### 2️⃣ Secure API Configuration
Create a `.env` file:
```env
SERPAPI_KEY=your_serpapi_key_here
TOP_N=20
KEYWORDS=smart fan,bldc fan,energy saving fan
```

### ▶️ Run Intelligence Pipeline
```bash
python main.py
```

### 📊 Launch Strategy Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 🧠 Technology Stack

* **Python**
* **SerpAPI** (Google Intelligence)
* **Sentence-Transformers** (MiniLM Semantic AI)
* **Transformers** (DistilBERT Sentiment NLP)
* **RapidFuzz** (High-performance fuzzy matching)
* **NumPy / Pandas** (Enterprise data processing)
* **Streamlit** (Executive dashboard)

---

## 🛣️ Atomberg Expansion Roadmap (Phase-2)

* Multi-platform SoV: YouTube, Amazon, Flipkart, Instagram
* Product-level SoV (Renesa, Gorilla, Studio series)
* City-wise geo-SoV tracking
* Historical trend modeling
* Campaign impact measurement
* Automated CMO insights email reporting
* Predictive market-share forecasting

---

## 📈 Strategic Value for Atomberg

This platform enables data-backed competitive decision-making by converting:

> **Unstructured Google search noise → Actionable brand dominance intelligence.**

It empowers Atomberg to proactively control digital mindshare, optimize marketing ROI, and strengthen leadership in the BLDC smart fan category.
