import polars as pl
import streamlit as st

from src.visualization import get_output_path

st.set_page_config(page_title="Imbalance Handling", page_icon="⚖️", layout="wide")

st.title("Step 4: Class Imbalance Handling")
st.caption("Testing whether resampling unlocks hidden signal")

st.markdown("""
All Phase 1 and Phase 2 models showed high recall and low precision - a pattern consistent
with class imbalance causing models to favour the majority class. But the imbalance ratio is
only ~2. Let's test the hypothesis rigorously.

Three resampling strategies were evaluated on the **engineered feature set** using the same
fixed train/test split, so results are directly comparable to the SVM baseline (0.548).

**Training set before resampling:** 537 clean vs 259 defective (IR = 2.07).
""")

st.divider()

tab1, tab2, tab3 = st.tabs([
    "1 - Random Undersampling",
    "2 - SMOTE Oversampling",
    "3 - BalancedBaggingClassifier",
])

with tab1:
    st.subheader("RandomUnderSampler + Random Forest")
    st.markdown("""
    Randomly remove majority-class rows until the training set is balanced
    (259 clean, 259 defective). Fit a Random Forest on the balanced set.
    """)
    c1, c2 = st.columns(2)
    c1.metric("ROC-AUC", "0.412", delta="-0.136 vs SVM baseline", delta_color="inverse")
    c2.metric("Training rows after sampling", "518", delta="-278 rows discarded")
    st.error("""
    **Why it failed:** Discarding 278 real majority-class samples (~35 % of training data)
    from an already small dataset (796 rows) left the Random Forest unable to learn reliable
    decision boundaries in an 18-dimensional space. Information loss outweighed any benefit
    from balance.
    """)

with tab2:
    st.subheader("SMOTE (k=5 neighbours) + Random Forest")
    st.markdown("""
    Synthesise 278 minority-class samples by interpolating between real defective modules
    in the engineered feature space, expanding training from 796 -> 1,074 rows (537 per class).
    """)
    c1, c2, c3 = st.columns(3)
    c1.metric("ROC-AUC", "0.453", delta="-0.095 vs SVM baseline", delta_color="inverse")
    c2.metric("Precision (1)", "0.300")
    c3.metric("F1 (weighted)", "0.526", delta="+0.367 vs SVM", delta_color="normal")
    st.warning("""
    **Partially helpful - but not where it counts:**
    SMOTE improved F1 substantially (better precision/recall balance) but ROC-AUC - the
    threshold-independent discriminative measure - did not improve.

    The synthetic minority samples were interpolated in a feature space with near-zero MI
    with the target. Interpolating between defective modules in a space where defectiveness
    is *not spatially clustered* creates misleading training signal.
    """)

with tab3:
    st.subheader("BalancedBaggingClassifier (300 shallow DTs, max_depth=5)")
    st.markdown("""
    An ensemble of shallow decision trees, each trained on a balanced bootstrap:
    majority class undersampled within each bootstrap, all minority samples used.
    No synthetic data.
    """)
    c1, c2 = st.columns(2)
    c1.metric("ROC-AUC", "0.436", delta="-0.112 vs SVM baseline", delta_color="inverse")
    c2.metric("F1 (weighted)", "0.486")
    st.error("""
    **Worse than SMOTE:** Each base learner trains on ~518 rows with depth-5 trees
    (max 31 leaves). Shallow trees in near-zero MI feature space find only spurious splits.
    The ensemble averages 300 near-random classifiers, converging to ~0.5 with added
    sampling noise pulling it below 0.45.
    """)

st.divider()

st.header("Summary comparison")

summary = pl.DataFrame({
    "Strategy": [
        "Undersampling (RF)",
        "BalancedBagging (DT)",
        "SMOTE (RF)",
        "SVM baseline (no resampling) ⭐",
    ],
    "ROC-AUC": [0.412, 0.436, 0.453, 0.548],
    "Precision (1)": [0.255, 0.308, 0.300, 0.325],
    "Recall (1)": [0.415, 0.508, 0.369, 1.000],
    "F1 (weighted)": [0.433, 0.486, 0.526, 0.159],
})
st.dataframe(summary, width='stretch', hide_index=True)

col1, col2 = st.columns(2)
with col1:
    p = get_output_path("resampling_comparison.png")
    if p.exists():
        st.image(str(p), caption="F1 and precision/recall comparison", width='stretch')
with col2:
    p = get_output_path("resampling_roc_overlay.png")
    if p.exists():
        st.image(str(p), caption="ROC curve overlay - all resampling strategies", width='stretch')

st.divider()

st.error("""
**Key finding: resampling is not the bottleneck.**

Every resampling strategy performed *worse* than the unsampled SVM on ROC-AUC.
This is diagnostic: when signal is absent, balancing the training distribution cannot
create information that was never there.

The bottleneck is not the class ratio - it is the **absence of discriminative signal
in the features**. We need a different diagnosis tool: Mutual Information.
""")
