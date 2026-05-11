import math
import polars as pl
import polars.selectors as cs
import dotenv
import os
from pathlib import Path

EPSILON = 1e-8
TARGET_COL = "DEFECT_LABEL"
RAW_FEATURE_COLS = [
    "LOC", "CYCLO", "LENGTH", "VOLUME", "DIFFICULTY",
    "INT_FAN_IN", "INT_FAN_OUT", "NUM_OPERATORS", "NUM_OPERANDS", "BRANCH_COUNT",
]


def load_raw_data(filename: str, fallback_dir: str = "data") -> pl.DataFrame | None:
    """
    Load raw data
    
    Args:
        filename (str): name of the raw dataset file
        fallback_dir (str): fallback directory in which the data is contained
            Look here if env file is not loaded correctly

    Returns:
        pl.DataFrame: dataframe related to source file
        None: If file does not exist or loading phase fails
    """
    dotenv.load_dotenv()

    env_dir = os.getenv("DATA_DIR")
    if env_dir is not None:
        data_folder = Path(env_dir)
    else:
        relative = Path(fallback_dir)
        if relative.exists():
            data_folder = relative
        else:
            # Resolve relative to this module so the app works from any working directory
            module_relative = Path(__file__).parent.parent.parent / "data"
            data_folder = module_relative if module_relative.exists() else relative

    path = data_folder / filename
    if not path.exists():
        return None
    try:
        return pl.read_csv(path)
    except Exception:
        return None


def clean_data(df: pl.DataFrame | None) -> pl.DataFrame | None:
    """
    Apply data cleaning transformations starting from a copy of the dataset
    received as input
    
    Args:
        df (pl.DataFrame): dataframe representing the loaded dataset

    Returns:
        pl.DataFrame: cleaned dataframe
    """
    if df is None or df.is_empty():
        return df
    
    ret = df.clone()
    numeric_df = ret.select(cs.numeric())
    
    for col in numeric_df.columns:
        ret = ret.with_columns(ret[col].fill_null(strategy="mean"))
    return ret


def remove_noisy_data(df: pl.DataFrame | None) -> pl.DataFrame | None:
    """
    Remove data with meaningless information or invalid ones

    Args:
        df (pl.DataFrame): dataframe representing the loaded dataset

    Returns:
        pl.DataFrame: cleaned dataframe
    """
    if df is None or df.is_empty():
        return df

    ret = df.clone()
    ret = ret.filter(pl.col("LOC") > 0)
    ret = ret.filter(pl.col("LENGTH") > 0)
    ret = ret.filter(pl.col("VOLUME") > 0)
    return ret


def engineer_features(df: pl.DataFrame) -> pl.DataFrame:
    """
    Add 8 domain-inspired engineered features to expose non-linear thresholds
    and multiplicative effects invisible to Pearson correlation

    Args:
        df (pl.DataFrame): cleaned dataframe with raw features

    Returns:
        pl.DataFrame: dataframe extended with engineered columns
    """
    ret = df.clone()
    ret = ret.with_columns([
        (pl.col("CYCLO") / (pl.col("LOC") + EPSILON)).alias("CYCLO_PER_LOC"),
        (pl.col("NUM_OPERATORS") / (pl.col("NUM_OPERANDS") + EPSILON)).alias("OPERATOR_RATIO"),
        (pl.col("VOLUME") / (pl.col("LENGTH") + EPSILON)).alias("CODE_DENSITY"),
        (pl.col("BRANCH_COUNT") * pl.col("CYCLO")).alias("CONTROL_COMPLEXITY"),
        (pl.col("INT_FAN_IN") + pl.col("INT_FAN_OUT")).alias("COUPLING"),
        (pl.col("VOLUME") * pl.col("DIFFICULTY")).alias("PROGRAM_EFFORT"),
        (pl.col("VOLUME") / (pl.col("DIFFICULTY") + EPSILON)).alias("INTELLIGENCE_CONTENT"),
        (
            pl.lit(171.0)
            - pl.lit(5.2) * (pl.col("VOLUME") + EPSILON).log(math.e)
            - pl.lit(0.23) * pl.col("CYCLO")
            - pl.lit(16.2) * (pl.col("LOC") + EPSILON).log(math.e)
        ).alias("MAINTAINABILITY_INDEX"),
    ])
    return ret


def prepare_ml_data(
    df: pl.DataFrame,
    feature_cols: list[str] | None = None,
) -> tuple:
    """
    Extract feature matrix and label vector for sklearn consumption

    Args:
        df (pl.DataFrame): processed dataframe
        feature_cols (list[str] | None): columns to use as features;
            defaults to all columns except TARGET_COL

    Returns:
        tuple: (X: np.ndarray, y: np.ndarray, feature_cols: list[str])
    """
    if feature_cols is None:
        feature_cols = [c for c in df.columns if c != TARGET_COL]
    X = df.select(feature_cols).to_numpy().astype(float)
    y = df[TARGET_COL].to_numpy().astype(int)
    return X, y, feature_cols
