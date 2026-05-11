import streamlit as st
import polars as pl

st.set_page_config(
    page_title="Software Defects Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Software Defects Analysis & Prediction")
st.caption("A binary classification study on five NASA MDP datasets - JM1, KC1, CM1, KC2, PC1")

st.markdown("""
This presentation walks through a complete ML pipeline built to predict whether a software
module contains defects using only **static code metrics**.

> **Spoiler:** despite exhaustive modelling, feature engineering, class-balancing, and mutual
> information selection, no approach exceeded ROC-AUC 0.548 - barely above the random baseline
> of 0.5. Here's the full story of *why*.
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Datasets merged", "5", help="JM1 · KC1 · CM1 · KC2 · PC1 (NASA MDP)")
col2.metric("Modules after cleaning", "996")
col3.metric("Class imbalance ratio", "≈ 2.07", help="67 % clean · 33 % defective")
col4.metric("Best ROC-AUC achieved", "0.548", delta="+0.048 vs random", delta_color="off")

st.divider()

st.subheader("The story in 5 steps")

data = {
    "Step": [
        "1 · Dataset & Cleaning",
        "2 · Exploratory Analysis",
        "3 · Baseline Models + Feature Engineering",
        "4 · Class Imbalance Handling",
        "5 · Mutual Information + Conclusions",
    ],
    "What we tried": [
        "Load five NASA datasets, apply quality filters, profile features and class balance",
        "Pearson correlation matrix, class-conditional distributions, VIF analysis",
        "Four model families in two phases: raw features then 8 engineered metrics",
        "SMOTE, random undersampling, and BalancedBaggingClassifier",
        "MI feature selection with bootstrap stability check and cross-validated k selection",
    ],
    "Key finding": [
        "996 clean modules, mild IR ≈ 2 - resampling *shouldn't* be necessary",
        "Max |r| = 0.07 - near-zero linear signal, no dominant non-linear predictor",
        "Best ROC-AUC 0.548 after engineering; SVM still predicts every module as defective",
        "Every resampling strategy underperformed the SVM baseline - IR is not the bottleneck",
        "Signal ceiling confirmed at ~0.55; root cause is data quality, not modelling choices",
    ],
}

st.dataframe(
    pl.DataFrame(data),
    width='stretch',
    hide_index=True,
)

st.divider()
st.info(
    "**Root cause:** Static structural metrics (LOC, cyclomatic complexity, coupling) describe "
    "*what* code looks like, not *how carefully* it was written. "
    "What's actually needed: **code churn, change history, and developer process data.**"
)

st.markdown("Use the **sidebar** to walk through each step in order.")
