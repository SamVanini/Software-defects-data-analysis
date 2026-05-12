import matplotlib.pyplot as plt
import polars as pl
import streamlit as st

from src.data_processing import clean_data, load_raw_data, remove_noisy_data

st.set_page_config(page_title="Dataset & Cleaning", page_icon="📊", layout="wide")

st.title("Step 1: Dataset & Cleaning")
st.caption("Five NASA MDP datasets merged into one binary classification problem")


@st.cache_data
def load_pipeline():
    df_raw = load_raw_data("dataset.csv")
    df_clean = clean_data(df_raw)
    df_final = remove_noisy_data(df_clean)
    return df_raw, df_clean, df_final


df_raw, df_clean, df = load_pipeline()

st.header("1.1  Source datasets")
st.markdown("""
Five **NASA Metrics Data Program (MDP)** datasets were merged into a single file:
**JM1**, **KC1**, **CM1**, **KC2**, and **PC1**.

These represent real-world software projects from NASA missions and are the standard
benchmark in empirical software engineering research. Each row is one software module
(function or file) described by static code metrics extracted by automated analysis tools.
""")

c1, c2, c3 = st.columns(3)
c1.metric("Raw rows", f"{len(df_raw):,}")
c2.metric("Rows after cleaning", f"{len(df):,}")
c3.metric("Features (+ 1 target)", str(len(df.columns) - 1))

st.divider()

st.header("1.2  Features")

feature_table = pl.DataFrame({
    "Feature": [
        "LOC", "CYCLO", "LENGTH", "VOLUME", "DIFFICULTY",
        "INT_FAN_IN", "INT_FAN_OUT", "NUM_OPERATORS", "NUM_OPERANDS",
        "BRANCH_COUNT", "DEFECT_LABEL",
    ],
    "Family": [
        "Size", "Complexity", "Halstead", "Halstead", "Halstead",
        "Coupling", "Coupling", "Halstead", "Halstead",
        "Complexity", "Target",
    ],
    "Description": [
        "Lines of code - module size",
        "Cyclomatic complexity - number of independent execution paths",
        "Total operators + operands (Halstead token count)",
        "Halstead volume - information content of the program",
        "Halstead difficulty - mental effort to understand the code",
        "Number of modules that call this module",
        "Number of modules this module calls",
        "Distinct operator types used",
        "Distinct operand types used",
        "Conditional branches",
        "1 = defective module, 0 = clean module",
    ],
})
st.dataframe(feature_table, width='stretch', hide_index=True)
st.caption(
    "All numeric features arrive **pre-normalised to [0, 1]** (min-max scaled in the source "
    "datasets). StandardScaler is re-applied downstream only for models that require "
    "zero-mean unit-variance input (Logistic Regression, SVM)."
)

st.divider()

st.header("1.3  Class distribution")

counts = df["DEFECT_LABEL"].value_counts().sort("DEFECT_LABEL")
clean_n = counts.filter(pl.col("DEFECT_LABEL") == 0)["count"][0]
defect_n = counts.filter(pl.col("DEFECT_LABEL") == 1)["count"][0]
total = len(df)

c1, c2, c3 = st.columns(3)
c1.metric("Clean modules (0)", f"{clean_n:,}", f"{clean_n / total * 100:.1f} %", delta_arrow="off")
c2.metric("Defective modules (1)", f"{defect_n:,}", f"{defect_n / total * 100:.1f} %", delta_arrow="off")
c3.metric("Imbalance ratio (IR)", f"{clean_n / defect_n:.2f}")

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(
    ["Clean (0)", "Defective (1)"],
    [clean_n, defect_n],
    color=["#2ecc71", "#e74c3c"],
    width=0.45,
)
for bar, val, pct in zip(bars, [clean_n, defect_n], [clean_n / total * 100, defect_n / total * 100]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 8,
        f"{val}  ({pct:.1f} %)",
        ha="center", va="bottom", fontsize=11,
    )
ax.set_ylabel("Module count")
ax.set_ylim(0, clean_n * 1.25)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
st.pyplot(fig, width='stretch')
plt.close(fig)

st.info(
    "An IR of ~2 is **mild** by industry standards - production systems often see IR > 10. "
    "At this level, most models can handle the imbalance without resampling. "
    "We test this assumption explicitly in Step 4."
)

st.divider()

st.header("1.4  Cleaning decisions")
st.markdown("""
**Two-stage cleaning pipeline:**

1. **Null imputation** - numeric nulls replaced with column mean (no nulls found in this dataset).
2. **Noisy row filter** - three conditions remove physically impossible entries:
""")

rows_removed = len(df_raw) - len(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("LOC = 0 -> removed", "", help="A module with zero lines of code is not real")
c2.metric("LENGTH = 0 -> removed", "", help="Zero token length is a data artefact")
c3.metric("VOLUME = 0 -> removed", "", help="Zero Halstead volume means no tokens")
c4.metric("Total rows removed", f"{rows_removed:,}", f"{rows_removed / len(df_raw) * 100:.1f} % of raw", delta_arrow="off", delta_color="primary")

st.markdown("""
A module with zero LOC, zero LENGTH, or zero VOLUME cannot represent a real software module.
These artefacts would poison any ratio-based engineered feature (e.g. CYCLO ÷ LOC → ∞).
""")

st.divider()

st.header("1.5  Data sample")
st.dataframe(df.head(10), width='stretch')
