import pytest
from src.data_processing import load_raw_data

def load_raw_data_not_existant_file_should_return_none():
    ...

def load_raw_data_not_existant_env_should_use_fallback():
    ...

def load_raw_data_existant_file_should_return_dataframe():
    ...