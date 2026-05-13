import polars as pl
import streamlit as st
from src.visualization import get_output_path

st.set_page_config(page_title="Model Training", page_icon="🤖", layout="wide")

st.title("Step 3: Baseline Models & Feature Engineering")
st.caption("Two phases: raw features, then 8 engineered metrics")

st.header("3.1  Model selection rationale")
st.markdown("""
Four families were chosen to cover the full bias-variance spectrum:
""")

rationale = pl.DataFrame({
    "Model": ["Logistic Regression", "Random Forest", "Gradient Boosting", "SVM"],
    "Why chosen": [
        "Linear baseline; interpretable coefficients; ElasticNet covers both L1 (sparse) and L2 (shrinkage)",
        "Non-linear, handles feature interactions, robust to noise; class_weight='balanced' built in",
        "Sequential ensemble; each tree corrects residuals of the previous; strong on tabular data",
        "Maximum-margin classifier with kernel trick; can model non-linear boundaries (rbf, poly, sigmoid)",
    ],
    "Search strategy": [
        "GridSearchCV - 35 combos (7 C values x 5 l1_ratio)",
        "RandomizedSearchCV - 50 iterations from continuous distributions",
        "GridSearchCV - 1 458 combinations (full cartesian)",
        "GridSearchCV - 180 combos (C x kernel x gamma x degree)",
    ],
})
st.dataframe(rationale, width='stretch', hide_index=True)

st.caption(
    "After hyperparameter search, `TunedThresholdClassifierCV` (sklearn ≥ 1.5) "
    "re-optimised the decision threshold for F1 via 5-fold CV. Tuned thresholds ranged "
    "from 0.15 to 0.29 - well below the default 0.5, compensating for class imbalance."
)

st.divider()

st.header("3.2  Phase 1 - Raw features (10 features)")

phase1 = pl.DataFrame({
    "Model": ["Logistic Regression", "Random Forest", "Gradient Boosting", "SVM ⭐ best"],
    "ROC-AUC": [0.461, 0.453, 0.471, 0.514],
    "Precision (1)": [0.323, 0.314, 0.310, 0.325],
    "Recall (1)": [0.815, 0.923, 0.800, 1.000],
    "F1 (weighted)": [0.340, 0.190, 0.299, 0.159],
    "Best CV params (highlights)": [
        "C=0.1, l1_ratio=1.0 (pure L1)",
        "363 trees, max_depth=10, bootstrap=False",
        "lr=0.1, depth=3, 100 trees",
        "C=1, sigmoid kernel, gamma='auto'",
    ],
})
st.dataframe(phase1, width='stretch', hide_index=True)

st.warning("""
**Diagnostic pattern: high recall + low precision + ROC-AUC ≈ 0.46–0.51**

This combination means every model learned to **predict "defective" for almost every sample**
rather than actually discriminating. The extreme case is SVM: Recall = 1.000 and
Precision = 0.325 - it classified *every single test module* as defective.

Why? With max |Pearson r| = 0.07, no linear or split-based rule can reliably separate the
classes. After threshold tuning to optimise F1, the optimal threshold drops to ~0.28,
causing most predictions to flip to class 1.
""")

st.divider()

st.header("3.3  Feature engineering - 8 new metrics")
st.markdown("""
**Motivation:** Pearson r only detects *linear* association. Defect-proneness may be driven
by *thresholds* and *interactions* - a module is risky when complexity is high *relative to
its size*, not when it is high in absolute terms. These effects are invisible to correlation
but potentially learnable by tree-based models.
""")

eng_features = pl.DataFrame({
    "Feature": [
        "CYCLO_PER_LOC", "OPERATOR_RATIO", "CODE_DENSITY", "CONTROL_COMPLEXITY",
        "COUPLING", "PROGRAM_EFFORT", "INTELLIGENCE_CONTENT", "MAINTAINABILITY_INDEX",
    ],
    "Formula": [
        "CYCLO / LOC", "NUM_OPERATORS / NUM_OPERANDS", "VOLUME / LENGTH",
        "BRANCH_COUNT x CYCLO", "INT_FAN_IN + INT_FAN_OUT", "VOLUME x DIFFICULTY",
        "VOLUME / DIFFICULTY", "171 - 5.2·ln(VOLUME) - 0.23·CYCLO - 16.2·ln(LOC)",
    ],
    "Domain meaning": [
        "Complexity density - tightly packed branching is riskier than spread-out branches",
        "Operator-heavy code is harder to reason about and more error-prone",
        "Information per token - dense code correlates with cognitive load",
        "Multiplicative risk: many branches + high cyclomatic = highest defect risk",
        "Total module coupling - more dependencies create more failure propagation points",
        "Halstead effort - mental activity needed to implement the algorithm",
        "Inverse of difficulty - inherent algorithmic complexity",
        "Industry-standard composite maintainability metric (Microsoft/SEI formula)",
    ],
})
st.dataframe(eng_features, width='stretch', hide_index=True)

p = get_output_path("correlation_heatmap_engineered_data.png")
if p.exists():
    st.image(str(p), caption="Correlation heatmap - engineered features", width='stretch')

st.caption(
    "ε = 1e-8 prevents division-by-zero without materially affecting values since all "
    "features are normalised to [0, 1]. Even after engineering, correlations with DEFECT_LABEL "
    "remain near zero - confirming there is no hidden non-linear structure exposed by these combinations."
)

st.divider()

st.header("3.4  Phase 2 - Engineered features (18 features)")

phase2 = pl.DataFrame({
    "Model": ["Logistic Regression", "Random Forest", "Gradient Boosting", "SVM ⭐ best"],
    "ROC-AUC": [0.461, 0.479, 0.486, 0.548],
    "Precision (1)": [0.327, 0.308, 0.304, 0.325],
    "Recall (1)": [0.815, 0.862, 0.754, 1.000],
    "F1 (weighted)": [0.355, 0.227, 0.319, 0.159],
    "Δ ROC-AUC vs Phase 1": ["+0.000", "+0.026", "+0.015", "+0.034"],
})
st.dataframe(phase2, width='stretch', hide_index=True)

col_img, col_text = st.columns([3, 2])
with col_img:
    p = get_output_path("model_comparison.png")
    if p.exists():
        st.image(str(p), width='stretch')
with col_text:
    st.markdown("""
    **What changed:**
    - Marginal ROC-AUC gains (+0.015 to +0.034) for tree-based models and SVM.
    - Feature engineering did surface *some* non-linear structure.
    - But SVM still predicts class 1 for all 200 test samples (Recall = 1.000).
    - The ceiling is ~0.55 - the same wall regardless of feature set.

    **Why engineering couldn't help more:**
    - Engineered features are *compositions* of near-zero-signal inputs.
    - When inputs carry minimal signal, multiplying/dividing them amplifies noise alongside any signal.
    - The enginereed correlation heatmap shows the same near-zero associations with DEFECT_LABEL.
    """)

st.info(
    "**Best model so far:** SVM with sigmoid kernel, ROC-AUC = 0.548 on engineered features. "
    "But it's a degenerate classifier - it predicts 'defective' for every module. "
    "Next: test whether class imbalance is hiding learnable signal."
)
