import pytest
import polars as pl
import numpy as np
from src.data_processing import load_raw_data, clean_data

def test_load_raw_data_not_existant_file_should_return_none():
    # Arrange
    non_existant_file = "notexistant.csv"

    # Act
    df = load_raw_data(non_existant_file)

    # Assert
    assert df is None

def test_load_raw_data_not_existant_data_dir_should_return_none(mock_env_data_dir):
    # Arrange
    file_name = "sample.csv"

    # Act
    df = load_raw_data(file_name)

    # Assert
    assert df is None

@pytest.fixture
def mock_env_data_dir(monkeypatch):
    monkeypatch.setenv("DATA_DIR", "notexistant")

def test_load_raw_data_not_existant_env_should_use_fallback(mock_del_data_dir):
    # Arrange
    file_name = "sample.csv"

    # Act
    df = load_raw_data(file_name)

    # Assert
    assert df is not None
    assert len(df.columns) >= 6
    assert len(df) > 0

@pytest.fixture
def mock_del_data_dir(monkeypatch):
    monkeypatch.delenv("DATA_DIR")

def test_load_raw_data_existant_file_should_return_dataframe():
    # Arrange
    file_name = "sample.csv"

    # Act
    df = load_raw_data(file_name)

    # Assert
    assert df is not None
    assert len(df.columns) >= 6
    assert len(df) > 0

def test_clean_data_none_dataframe_should_return_none():
    # Arrange
    mock_schema = pl.Schema({"x": pl.Int32(), "y": pl.String()})
    empty_df = mock_schema.to_frame()

    # Act
    df = clean_data(empty_df)

    assert df.equals(empty_df)

def test_clean_data_numeric_null_cols_should_be_filled_with_mean():
    # Arrange
    num_rows = 20
    random_data = []
    for n in np.random.randint(0, 100, num_rows):
        val = n if n % 2 == 0 else None
        random_data.append(val)

    mock_df = pl.DataFrame({"random_values": random_data})
    mock_df = mock_df.with_columns(
        pl.col("random_values").cast(pl.Float64)
    )

    # Act
    df = clean_data(mock_df)

    # Assert
    assert mock_df.null_count().sum().item() > 0
    assert df.null_count().sum().item() == 0