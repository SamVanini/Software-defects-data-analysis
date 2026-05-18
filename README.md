# Project: Software defects data analysis and prediction

Data analysis and binary classification models comparison. Project for Programming course, M.Sc. Data Science @ UniVR

## Project Overview

The project has the goal of analyze a dataset compiled from five widely-used software defect datasets: JM1, KC1, CM1, KC2, and PC1, originally collected from NASA’s Metrics Data Program (MDP). These datasets contain static code metrics extracted from real-world software modules, paired with binary defect labels indicating whether each module contains defects (1) or not (0).

After the exploration and binary classification models comparison, a Streamlit presentation has been created to show the outcome of the analysis without going into techincal details and keeping the coding details out of the way

## Project Structure

```
Software-defects-data-analysis/
├── notebooks/
│   └── data_workflow.ipynb          # Main workflow notebook
├── data/
│   └── sample.csv                   # Dataset for setup testing
|   └── dataset.csv                  # Dataset
├── env/                             # Virtual environment (created by setup script)
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
│   │   ├── test_data_processing.py
│   │   └── test_visualization.py
|   ├── docker-compose.yaml
|   ├── Dockerfile
│   └── Home.py
├── requirements.txt                 # Python dependencies
├── setup.sh                         # Linux/Mac setup script via python venv
├── setup.bat                        # Windows setup script via python venv
├── setup_uv.sh                      # Linux/Mac setup script via uv
├── setup_uv.bat                     # Windows setup script via uv
├── test_setup.py                    # Validation script
├── .env                             # Environment variables (optional)
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## How to run the project

### Project Setup (Python venv)

```bash
# Clone the **repository**
git clone <your-repo-url>
cd local-data-engineering-environment

# Run the automated setup script
./setup.sh  # Linux/Mac
# OR
setup.bat   # Windows
```

### Project Setup (uv)

```bash
# Clone the **repository**
git clone <your-repo-url>
cd local-data-engineering-environment

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

Tests live in `streamlit_app/tests/` and must be run from the `streamlit_app/` directory
so that `src.*` imports resolve correctly.

### Python venv

```bash
source env/bin/activate  # Linux/Mac
# OR
env\Scripts\activate.bat  # Windows

cd streamlit_app
pytest tests/
```

### uv

```bash
cd streamlit_app
uv run pytest tests/
```
