import polars as pl
import streamlit as st

from src.visualization import get_output_path

st.set_page_config(page_title="MI Selection & Conclusions", page_icon="🧬", layout="wide")

st.title("Step 5: Mutual Information Feature Selection")
st.caption("Ruling out every remaining hypothesis - and drawing the final verdict")

st.markdown("""
Pearson correlation measures *linear* dependence. Mutual Information (MI) quantifies
*any* statistical dependence - including non-linear and non-monotonic relationships.
For software metrics, defect rates might peak at intermediate complexity values rather
than monotonically at extremes. MI could reveal signal that correlation missed entirely.
""")

st.divider()

st.header("5.1  Single-run MI scores")

col_img, col_text = st.columns([3, 2])
with col_img:
    p = get_output_path("mi_scores.png")
    if p.exists():
        st.image(str(p), width='stretch')
with col_text:
    st.markdown("""
    MI was computed using `mutual_info_classif` with k=10 nearest neighbours
    (more stable than the default k=5 on small datasets).

    The single-run result is striking:

    - Highest score: **VOLUME = 0.025** - negligibly small.
    - Most features report **MI = 0.000** exactly.
    - Features at zero MI: CYCLO, LENGTH, CYCLO_PER_LOC, OPERATOR_RATIO,
      CONTROL_COMPLEXITY, CODE_DENSITY, INTELLIGENCE_CONTENT, MAINTAINABILITY_INDEX.

    MI scores this close to zero indicate that knowing the feature value provides
    almost no reduction in uncertainty about the defect label.

    But single-run MI on ~800 rows has high variance due to k-NN density estimation.
    We need a bootstrap to see the true picture.
    """)

st.divider()

st.header("5.2  Bootstrap stability check (100 iterations)")

col_img, col_text = st.columns([3, 2])
with col_img:
    p = get_output_path("mi_bootstrap.png")
    if p.exists():
        st.image(str(p), width='stretch')
with col_text:
    st.markdown("""
    100 bootstrap iterations reveal the **true mean ranking**:

    | Rank | Feature | Mean MI |
    |------|---------|---------|
    | 1 | VOLUME | 0.065 |
    | 2 | LOC | 0.052 |
    | 3 | PROGRAM_EFFORT | 0.051 |
    | 4 | DIFFICULTY | 0.050 |
    | 5 | INTELLIGENCE_CONTENT | 0.044 |
    | 6 | CYCLO_PER_LOC | 0.043 |
    | 7 | NUM_OPERANDS | 0.043 |
    | 8 | OPERATOR_RATIO | 0.042 |
    | ... | ... | ... |

    **Critical observation:** The single-run zeros were estimation noise.
    All features carry *similar, uniformly low MI* (~0.040-0.065).

    There is no clearly dominant feature. The differences between ranks are
    within bootstrap variance. **There is no hidden non-linear predictor
    lurking in the data** - the signal is genuinely weak and diffuse.
    """)

st.divider()

st.header("5.3  Cross-validated feature count selection")

st.markdown("""
A `Pipeline(SMOTE → SelectKBest(MI) → RandomForest)` was embedded inside
`GridSearchCV` to find the optimal number of features k ∈ {4, 6, 8, 10, 12, 15, 18}
**without data leakage** - SMOTE is inside the pipeline so synthetic samples are
generated only on training folds, never on validation folds.
""")

c1, c2, c3 = st.columns(3)
c1.metric("Best k", "8")
c2.metric("Best CV ROC-AUC", "0.548")
c3.metric("Test ROC-AUC", "0.545")

st.markdown("""
**Selected features (k=8):**
`CYCLO · VOLUME · INT_FAN_IN · INT_FAN_OUT · BRANCH_COUNT ·
CONTROL_COMPLEXITY · COUPLING · MAINTAINABILITY_INDEX`
""")

col_img, col_text = st.columns([3, 2])
with col_img:
    p = get_output_path("mi_feature_selection_roc.png")
    if p.exists():
        st.image(str(p), caption="ROC-AUC vs number of selected features", width='stretch')
with col_text:
    final_comparison = pl.DataFrame({
        "Strategy": [
            "SMOTE + all 18 features",
            "SMOTE + MI top-8 features",
            "SVM (no resampling, engineered) ⭐",
        ],
        "ROC-AUC": [0.453, 0.545, 0.548],
    })
    st.dataframe(final_comparison, width='stretch', hide_index=True)
    st.markdown("""
    SMOTE + MI recovered from 0.453 → 0.545 simply by removing noisy features,
    but converged to the **same ceiling** as the SVM baseline.

    Dropping 10 low-MI features reduced model variance without adding signal.
    This confirms ~8 features have marginally useful information and the rest
    are pure noise contributors.

    The ROC-AUC is unchanged after selection →
    **Signal ceiling is a data problem, not a feature problem.**
    """)

st.divider()

st.header("5.4  Root cause analysis")

st.markdown("""
All modelling interventions - hyperparameter tuning, feature engineering, class balancing,
and mutual information selection - converged to the same ceiling of **ROC-AUC ≈ 0.55**.
This consistency across fundamentally different model families and methodologies is
strong evidence that the ceiling is **intrinsic to the data, not an implementation artefact.**
""")

root_causes = pl.DataFrame({
    "Factor": [
        "Feature-label near-zero correlation (r ≤ 0.07)",
        "Uniformly low MI (all features ≤ 0.065)",
        "Multi-project aggregation (5 datasets)",
        "Small sample size (n = 996)",
        "Pre-normalised features [0, 1]",
        "Absence of dynamic/process metrics",
    ],
    "Evidence": [
        "Pearson heatmap - Step 2",
        "Bootstrap MI analysis - Step 5",
        "Dataset description - Step 1",
        "Data loading step",
        "Data format description",
        "Domain knowledge + SE literature",
    ],
    "Impact": [
        "Linear models structurally limited",
        "Non-linear models also limited",
        "Defect distributions vary by project, team, tooling - merging adds heterogeneity noise",
        "k-NN MI estimation and SMOTE interpolation both degrade on small n",
        "Min-max scaling compresses outliers that may carry useful extreme-value signals",
        "Static metrics capture structure, not the engineering process that introduces bugs",
    ],
})
st.dataframe(root_causes, width='stretch', hide_index=True)

st.divider()

st.header("5.5  Final verdict & what would actually help")

st.error("""
**Static structural metrics do not carry enough information to reliably predict software defects.**

Every technique correctly diagnosed or partially compensated for a specific limitation
(linearity, scale sensitivity, imbalance, noise) but none could *create* signal that is
absent at the source.
""")

st.subheader("All phases - summary")
all_phases = pl.DataFrame({
    "Phase": [
        "Phase 1: Raw features",
        "Phase 2: Engineered features",
        "Step 4: Resampling",
        "Step 5: MI selection",
    ],
    "Best model": [
        "SVM (sigmoid)",
        "SVM (sigmoid)",
        "SVM baseline (no resampling)",
        "SMOTE + RF (k=8)",
    ],
    "ROC-AUC": [0.514, 0.548, 0.548, 0.545],
    "Key finding": [
        "All models near-random; SVM predicts class 1 universally",
        "Marginal gains from interaction terms; same ceiling",
        "All resampling strategies underperformed; IR=2 is not the bottleneck",
        "Signal confirmed uniformly low; no hidden non-linear predictor found",
    ],
})
st.dataframe(all_phases, width='stretch', hide_index=True)

st.subheader("What would actually help")
st.success("""
**1. Process metrics (highest impact)**
Add change history (commits, authors, time since last change), code churn (lines added/
deleted/modified), and test coverage. These are consistently the strongest defect predictors
in the empirical SE literature.

**2. More data from fewer projects**
Instead of 5 small mixed datasets, a deeper dataset from a single codebase removes
cross-project heterogeneity. Defect distributions vary dramatically by team and tooling.

**3. Bug-type labels**
Distinguishing security bugs from logic bugs from interface bugs enables specialised
models rather than a single undifferentiated classifier.

**4. Ensemble stacking (if stuck with these features)**
A stacked ensemble of the top performers (SVM + SMOTE+MI RF) may squeeze out a few
additional ROC-AUC points by combining complementary error patterns - but the signal
ceiling remains; this is a marginal gain only.
""")
