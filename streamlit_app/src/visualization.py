import os
from pathlib import Path
import dotenv


def get_output_path(filename: str) -> Path:
    """
    Resolve the absolute path to a pre-generated output image.

    Try to retrieve file path from environment variable, otherwise it uses fallback
    The fallback output/ directory lives at the project root, two levels above
    this module (streamlit_app/src/visualization.py -> project root).

    Args:
        filename (str): name of the resource to retrieve

    Returns:
        Path: path to the requested resource
    """
    dotenv.load_dotenv()
    env_dir = os.getenv("OUTPUT_DIR")

    if env_dir is not None:
        return Path(env_dir) / filename

    # Local dev fallback: should be removed in favour of envirnoment variables
    return Path(__file__).parent.parent.parent / "output" / filename
