import streamlit as st
from src.visualization import get_output_path

st.set_page_config(page_title="Exploratory Analysis", page_icon="🔍", layout="wide")

st.title("Step 2: Exploratory Data Analysis")
st.caption("Searching for signal before touching a model")

st.markdown("""
Before selecting a model, we need to understand whether the features carry any predictive
signal at all. Two complementary analyses answer this:

1. **Pearson correlation** - detects linear association between each feature and the target.
2. **Mean feature value per class** - reveals whether defective and clean modules live in
   different parts of feature space, even non-linearly.
""")

st.divider()

st.header("2.1  Pearson correlation - raw features")

col_img, col_text = st.columns([3, 2])
with col_img:
    p = get_output_path("correlation_heatmap.png")
    if p.exists():
        st.image(str(p), width='stretch')
    else:
        st.warning(f"Image not found: {p}")

with col_text:
    st.markdown("""
    **Key observations:**

    - The two highest absolute correlations with `DEFECT_LABEL` are:
      - `NUM_OPERANDS` ↔ label: **r = -0.07**
      - `BRANCH_COUNT` ↔ label: **r = +0.06**
    - These values are effectively zero.
    - Strong **inter-feature** correlations exist (e.g. VOLUME ↔ LENGTH ≈ 0.95,
      NUM_OPERATORS ↔ NUM_OPERANDS ≈ 0.88), indicating high redundancy - but
      no useful signal leaking through to the label.

    **Implication for models:**

    - Linear models (Logistic Regression, SVM with linear kernel) face a
      fundamental obstacle: there is no linear combination of features that
      separates the classes.
    - Tree-based models still need *some* monotonic relationship at each split.
      Near-zero Pearson r is a warning sign even for them.
    """)

st.divider()

st.header("2.2  Mean feature value per class")

col_img, col_text = st.columns([3, 2])
with col_img:
    p = get_output_path("diverging_barchart.png")
    if p.exists():
        st.image(str(p), width='stretch')
    else:
        st.warning(f"Image not found: {p}")

with col_text:
    st.markdown("""
    The diverging bar chart shows the **difference in mean feature value** between
    defective (1) and clean (0) modules.

    - Most features show a small positive offset for defective modules - larger,
      more complex modules are slightly more likely to be defective.
    - But the differences are tiny relative to feature variance; the distributions
      overlap almost completely.
    - `NUM_OPERANDS` is the only feature with a notable *negative* offset
      (defective modules slightly lower), consistent with r = -0.07.
    """)

st.divider()

st.header("2.3  Feature distributions per class")

p = get_output_path("feature_distribution_perclass.png")
if p.exists():
    st.image(str(p), width='stretch')
else:
    st.warning(f"Image not found: {p}")

st.markdown("""
The violin/KDE plots confirm what correlation analysis hinted at: **the class-conditional
distributions are almost identical for every feature.** There is no feature whose value
clearly separates defective from clean modules.

This is the most direct visual evidence that the raw feature set lacks discriminative power.
""")

st.divider()

st.header("2.4  What this means for modelling")

st.error("""
**Near-zero linear signal is a serious warning.** It does not rule out non-linear
relationships - tree-based models can exploit those. But it sets expectations low.

The next step is to test four model families and see how they perform on raw features.
If even non-linear models fail, the bottleneck is the features themselves, not the choice
of algorithm.
""")
