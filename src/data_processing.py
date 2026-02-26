import polars as pl
import dotenv
import os
from pathlib import Path

def load_raw_data(filename: str, fallback_dir: str = "data") -> pl.DataFrame | None:
    """
    Load raw data
    
    Args:
        filename (str): name of the raw dataset file
        fallback_dir (str): fallback directory in which the data is contained
            Look here if env file is not loaded correctly

    Returns:
        pl.DataFrame: dataframe related to source file
        None: If file does not exists or loading phase fails
    """
    dotenv.load_dotenv()

    data_folder = os.getenv("DATA_DIR") or fallback_dir
    path = Path(data_folder).joinpath(filename)
    
    if Path(path).exists() == False:
        # TODO: set up logger to log error
        return None
    try:
        df = pl.read_csv(path)
        return df
    except:
        # TODO: set up logger to log exception
        return None
        
def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    """Apply data cleaning transformations"""
    ...