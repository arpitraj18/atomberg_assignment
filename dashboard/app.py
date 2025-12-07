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
    file_path = "data/raw_google_results.csv"
    if not os.path.exists(file_path):
        st.error("❌ No data found. Please upload 'data/raw_google_results.csv' in the repository.")
        return pd.DataFrame()
    return pd.read_csv(file_path)


# -----------------------------------------------------
# MAIN DASHBOARD
# -----------------------------------------------------
def main():
    st.title("Smart Fan – Google Search Share of Voice Dashboard")


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