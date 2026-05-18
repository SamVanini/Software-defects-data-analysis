import pytest
from pathlib import Path
from src.visualization import get_output_path


def test_get_output_path_returns_path_object():
    result = get_output_path("test.png")
    assert isinstance(result, Path)


def test_get_output_path_filename_is_last_component():
    filename = "correlation_heatmap.png"
    result = get_output_path(filename)
    assert result.name == filename


def test_get_output_path_parent_is_output_dir():
    result = get_output_path("any_file.png")
    assert result.parent.name == "output"


def test_get_output_path_is_absolute():
    result = get_output_path("test.png")
    assert result.is_absolute()


def test_get_output_path_different_filenames_produce_different_paths():
    result_a = get_output_path("file_a.png")
    result_b = get_output_path("file_b.png")
    assert result_a != result_b


@pytest.mark.parametrize("filename", [
    "correlation_heatmap.png",
    "model_comparison.png",
    "mi_scores.png",
    "resampling_comparison.png",
    "mi_feature_selection_roc.png",
])
def test_get_output_path_known_output_files_exist(filename):
    p = get_output_path(filename)
    assert p.exists(), f"Expected output file not found: {p}"
