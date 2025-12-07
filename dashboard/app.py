# dashboard/app.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from analytics.sov_metrics import compute_sov, compute_sov_by_keyword
from analytics.insights import generate_insights


# -----------------------------------------------------
# SAFE DATA LOADING (no crash if file missing)
# -----------------------------------------------------
@st.cache_data
def load_data():
    if not os.path.exists("data/raw_google_results.csv"):
        st.warning("No data found yet. Click 'Refresh Google Results' to fetch new data.")
        return pd.DataFrame()
    return pd.read_csv("data/raw_google_results.csv")


# -----------------------------------------------------
# MAIN DASHBOARD
# -----------------------------------------------------
def main():
    st.title("Smart Fan – Google Search Share of Voice Dashboard")

    # ---------- Refresh Button ----------
    st.sidebar.header("Data Update")

    if st.sidebar.button("🔄 Refresh Google Results"):
        from ingestion.google_search import fetch_google_results
        from config import KEYWORDS
        from processing.text_cleaning import clean_text
        from processing.sentiment import sentiment_score
        from processing.brand_detection import detect_brand

        st.info("Fetching fresh Google Search results...")

        all_rows = []
        for kw in KEYWORDS:
            rows = fetch_google_results(kw)
            all_rows.extend(rows)

        df_new = pd.DataFrame(all_rows)
        df_new["text"] = df_new["title"].fillna("") + " " + df_new["snippet"].fillna("")
        df_new["clean_text"] = df_new["text"].apply(clean_text)
        df_new["sentiment"] = df_new["clean_text"].apply(sentiment_score)
        df_new["brand"] = df_new.apply(lambda r: detect_brand(r["clean_text"], r["sentiment"]), axis=1)

        os.makedirs("data", exist_ok=True)
        df_new.to_csv("data/raw_google_results.csv", index=False)

        st.success("Data refreshed successfully! Reload the page to see updates.")

    # ---------- Load Data ----------
    df = load_data()
    if df.empty:
        return  # stop if dataset missing

    # ---------- Sidebar Filters ----------
    platforms = st.sidebar.multiselect(
        "Platform",
        options=sorted(df["platform"].unique()),
        default=list(sorted(df["platform"].unique()))
    )
    keywords = st.sidebar.multiselect(
        "Keywords",
        options=sorted(df["keyword"].unique()),
        default=list(sorted(df["keyword"].unique()))
    )

    df_f = df[df["platform"].isin(platforms) & df["keyword"].isin(keywords)]

    st.subheader("Raw Search Results (Filtered)")
    st.dataframe(df_f[["platform", "keyword", "rank", "title", "snippet", "brand", "sentiment"]])

    st.subheader("Global SOV (Filtered)")
    sov_global = compute_sov(df_f)
    st.dataframe(sov_global)
    if not sov_global.empty:
        st.bar_chart(sov_global.set_index("brand")[["sov_volume"]])
        st.bar_chart(sov_global.set_index("brand")[["sov_visibility"]])
        st.bar_chart(sov_global.set_index("brand")[["sov_positive"]])

    st.subheader("SOV by Keyword (Filtered)")
    sov_kw = compute_sov_by_keyword(df_f)
    if not sov_kw.empty:
        st.dataframe(sov_kw)

    st.subheader("Automated Insights")
    insights_md = generate_insights(df_f, sov_global, sov_kw)
    st.markdown(insights_md)


if __name__ == "__main__":
    main()