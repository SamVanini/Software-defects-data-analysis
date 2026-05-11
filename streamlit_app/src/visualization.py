from pathlib import Path


def get_output_path(filename: str) -> Path:
    """
    Resolve the absolute path to a pre-generated output image.

    The output/ directory lives at the project root, two levels above
    this module (streamlit_app/src/visualization.py -> project root).
    """
    return Path(__file__).parent.parent.parent / "output" / filename
