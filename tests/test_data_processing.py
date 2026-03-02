import pytest
from src.data_processing import load_raw_data

def test_load_raw_data_not_existant_file_should_return_none():
    # Arrange
    non_existant_file = "notexistant.csv"

    # Act
    df = load_raw_data(non_existant_file)

    # Assert
    assert df is None

def test_load_raw_data_not_existant_env_should_use_fallback(mock_env_data_dir):
    # Arrange
    file_name = "sample.csv"

    # Act
    df = load_raw_data(file_name)

    #Assert
    assert df is None

@pytest.fixture
def mock_env_data_dir(monkeypatch):
    monkeypatch.setenv("DATA_DIR", "notexistant")

def test_load_raw_data_existant_file_should_return_dataframe():
    # Arrange
    file_name = "sample.csv"

    # Act
    df = load_raw_data(file_name)

    # Assert
    assert df is not None
    assert len(df.columns) >= 6
    assert len(df) > 0