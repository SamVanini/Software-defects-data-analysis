# Project: Software defects data analysis and prediction

Data analysis and binary classification models comparison. Project for Programming course, M.Sc. Data Science @ UniVR

## Project Overview

## Project Structure

```
Software-defects-data-analysis/
├── notebooks/
│   └── data_workflow.ipynb          # Main workflow notebook
├── data/
│   └── sample.csv                   # Dataset for setup testing
|   └──                              # Dataset
├── env/                             # Virtual environment (created)
├── output/                          # Generated outputs (created)
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

### Launch Jupyter

```bash
# Activate virtual environment
source env/bin/activate  # Linux/Mac
# OR
env\Scripts\activate.bat  # Windows

# Start Jupyter notebook
jupyter notebook
```

### Run the Workflow

Open and execute `notebooks/data_workflow.ipynb`