# Project: Software defects data analysis and prediction

Data analysis and binary classification models comparison. Project for Programming course, M.Sc. Data Science @ UniVR

## Project Overview

The project has the goal of analyze a dataset compiled from five widely-used software defect datasets: JM1, KC1, CM1, KC2, and PC1, originally collected from NASA’s Metrics Data Program (MDP). These datasets contain static code metrics extracted from real-world software modules, paired with binary defect labels indicating whether each module contains defects (1) or not (0).

After the exploration and binary classification models comparison, a Streamlit presentation has been created to show the outcome of the analysis without going into techincal details and keeping the coding details out of the way

## Project Structure

```
Software-defects-data-analysis/
├── data/
│   └── sample.csv                   # Dataset for setup testing
|   └── dataset.csv                  # Dataset
├── env/                             # Virtual environment (created by setup script)
├── notebooks/
│   └── data_workflow.ipynb          # Main workflow notebook
├── notes/
│   └── reasoning.md                 # Notes related to workflow trials
├── output/                          # Pre-generated plot images (loaded by Streamlit pages)
├── streamlit_app/                   # Streamlit presentation
│   ├── .streamlit/
|   │   └── config.toml              # Config file
|   ├── pages/                       # MPA Pages files
│   │   ├── 1_Dataset_and_Cleaning.py
│   │   ├── 2_Exploratory_Analysis.py
│   │   ├── 3_Baseline_Models_and_Feature_Engineering.py
│   │   ├── 4_Class_Imbalance_Handling.py
│   │   └── 5_Mutual_Information_and_Conclusions.py
|   ├── src/                         # Core functions used by the app
│   │   ├── data_processing.py
│   │   └── visualization.py
|   ├── tests/                       # Unit tests for core functions
│   │   ├── __init__.py
│   │   ├── test_data_processing.py
│   │   └── test_visualization.py
|   ├── docker-compose.yaml
|   ├── Dockerfile
│   └── Home.py
├── .env                             # Environment variables (optional)
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── setup_uv.sh                      # Linux/Mac setup script via uv
├── setup_uv.bat                     # Windows setup script via uv
├── setup.sh                         # Linux/Mac setup script via python venv
├── setup.bat                        # Windows setup script via python venv
└── test_environment.py              # Validation script
```

## How to run the project

### Project Setup (Python venv)

```bash
# Clone the **repository**
git clone <your-repo-url>
cd Software-defects-data-analysis

# Run the automated setup script
./setup.sh  # Linux/Mac
# OR
setup.bat   # Windows
```

### Project Setup (uv)

```bash
# Clone the **repository**
git clone <your-repo-url>
cd Software-defects-data-analysis

# Run the automated setup script
./setup_uv.sh  # Linux/Mac
# OR
setup_uv.bat   # Windows
```

### Launch Jupyter (Python venv)

```bash
# Activate virtual environment
source env/bin/activate  # Linux/Mac
# OR
env\Scripts\activate.bat  # Windows

# Start Jupyter notebook
jupyter notebook
```

### Launch Jupyter (uv)

`uv run jupyter notebook`

### Run the Workflow

Open and execute `notebooks/data_workflow.ipynb`

---

## Launch the Streamlit presentation

### Option 1 — Docker (recommended, no local Python required)

```bash
# From the project root
cd streamlit_app
docker compose up --build
```

The app will be available at **http://localhost:8501**.

To stop it:

```bash
docker compose down
```

> **Note:** the build context is the project root (see `docker-compose.yaml`), so the
> command must be run from inside `streamlit_app/`.

### Option 2 — Local (Python venv)

```bash
# Activate virtual environment
source env/bin/activate  # Linux/Mac
# OR
env\Scripts\activate.bat  # Windows

streamlit run streamlit_app/Home.py
```

### Option 3 — Local (uv)

```bash
uv run streamlit run streamlit_app/Home.py
```

The app will be available at **http://localhost:8501** in both local options.

---

## Run the tests

Tests live in `streamlit_app/tests/`. They can be run from either the project root or the
`streamlit_app/` subdirectory — pytest adds the test file's parent to `sys.path` automatically,
so `src.*` imports resolve correctly in both cases.

> **Note:** the Python venv setup (`setup.bat` / `setup.sh`) requires **Python 3.12 or higher**.
> Using an older Python will fail at the `polars` installation step.

### Python venv

```bash
source env/bin/activate  # Linux/Mac
# OR
env\Scripts\activate.bat  # Windows

# From the project root:
pytest streamlit_app/tests/

# Or from inside streamlit_app/:
cd streamlit_app
pytest tests/
```

### uv

```bash
# From the project root:
uv run pytest streamlit_app/tests/

# Or from inside streamlit_app/:
cd streamlit_app
uv run pytest tests/
```
