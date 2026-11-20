"""Interactive three-page portfolio companion dashboard (does not replace Power BI .pbix)."""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
st.set_page_config(page_title="Chegg vs ChatGPT | Analytics", page_icon="📊", layout="wide")
st.title("Chegg vs ChatGPT — AI Disruption & Learning Analytics")
st.caption("Reproducible portfolio dashboard. Observed results and assumption-based scenarios are labeled separately.")
page = st.sidebar.radio("Navigate", ["Chegg financials", "Student learning", "Stock & market strategy"])

def load(path):
    return pd.read_csv(path) if path.exists() else None

if page == "Chegg financials":
    st.header("1 — Financial disruption")
    df = load(OUT / "financial_powerbi.csv")
    if df is None:
        st.warning("Run python scripts/run_financial.py first")
        st.stop()
    df = df.sort_values("quarter")
    start, end = df.iloc[0], df.iloc[-1]
    a, b = st.columns(2)
    a.metric("Revenue decline (Q4 2022 → Q4 2024)", f"{(1-end.revenue_million/start.revenue_million)*100:.2f}%")
    b.metric("Subscribers decline (same window)", f"{(1-end.subscribers/start.subscribers)*100:.2f}%")
    st.subheader("Quarterly revenue ($M)")
    st.line_chart(df.set_index("quarter")["revenue_million"])
    st.subheader("Subscriber metric (quarterly reported count)")
    st.line_chart(df.set_index("quarter")["subscribers"])
    st.info("Working investor-sheet figures need source-level reconciliation. Timing does not prove ChatGPT caused the changes.")
elif page == "Student learning":
    st.header("2 — ASSISTments learning outcomes")
    mastery = load(OUT / "final_mastery_comparison.csv")
    hints = load(OUT / "assistments_help_groups.csv")
    next_acc = load(OUT / "assistments_next_opportunity_accuracy.csv")
    audit = load(OUT / "assistments_data_audit.csv")
    if mastery is None:
        st.warning("Original ASSISTments CSV has not been analyzed. Run python scripts/run_learning.py path/to/file.csv. No fake findings are displayed.")
        st.stop()
    if audit is not None:
        st.dataframe(audit, hide_index=True)
    if hints is not None:
        st.subheader("Hint category interactions")
        st.bar_chart(hints.set_index("help_group")["interactions"])
    if next_acc is not None:
        st.subheader("Later first-attempt accuracy (%)")
        st.bar_chart(next_acc.set_index("help_group")["next_accuracy_pct"])
    st.subheader("Operational mastery (three consecutive correct first responses)")
    st.dataframe(mastery, hide_index=True)
    st.bar_chart(mastery.set_index("help_group")["mastery_rate_pct"])
    st.info("Observational comparisons are not causal; group selection, prior ability, problem difficulty, and right-censoring matter.")
else:
    st.header("3 — Stock performance & market sizing")
    prices = load(OUT / "chegg_stock_history.csv")
    summary = load(OUT / "stock_decline_summary.csv")
    if prices is None or summary is None:
        st.warning("Stock data not available. Run python scripts/run_stock.py --download (requires internet), or supply a sourced adjusted-close CSV.")
    else:
        st.metric("Historical adjusted-close decline", f"{summary.iloc[0].peak_to_end_decline_pct:.2f}%")
        st.caption(f"Peak: {summary.iloc[0].peak_date}; end: {summary.iloc[0].end_date}; both adjusted closes")
        st.line_chart(prices.set_index("Date")["Close"])
    market = load(OUT / "india_testprep_market_scenarios.csv")
    if market is None:
        st.warning("Run python scripts/run_market.py first")
    else:
        st.subheader("Illustrative annual digital-product opportunity")
        st.bar_chart(market.set_index("scenario")["opportunity_crore"])
        st.dataframe(market, hide_index=True)
        st.info("₹2,000 Cr base case assumes 10 million annual paying learners × ₹2,000 each. It is NOT verified total Indian online test-prep TAM.")
    st.markdown("**Product pivot hypothesis:** progressive hints, personalized mastery practice, localized mock exams; validate through A/B tests, retention and willingness-to-pay research.")
