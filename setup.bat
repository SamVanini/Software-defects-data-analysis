@ECHO OFF
REM ============================================
REM Python-based Virtual Environment Setup Script
REM ============================================
REM This script creates a Python virtual environment using
REM venv and installs all required dependencies.
REM
REM Prerequisites: Python must be installed
REM Install Python: http://python.org/downloads/
REM ============================================

ECHO.
ECHO ========================================
ECHO Python Virtual Environment Setup
ECHO ========================================
ECHO.

REM Check if Python is installed
ECHO [1/7] Checking if Python is installed...
python --version >nul 2>&1

if ERRORLEVEL 1 (
    ECHO.
    ECHO [ERROR] Python is not installed or not in PATH!
    ECHO.
    ECHO Please install Python first:
    ECHO   - Visit: http://python.org/downloads/
    ECHO.
    PAUSE
    EXIT /b 1
)

REM Create virtual environment using Python
ECHO [2/7] Creating virtual environment with Python...
python -m venv env

if ERRORLEVEL 1 (
    ECHO [ERROR] Failed to create virtual environment!
    PAUSE
    EXIT /b 1
)

ECHO Virtual environment created successfully
ECHO.

REM Activate virtual environment
ECHO [3/7] Activating virtual environment...
CALL env\Scripts\activate.bat

if ERRORLEVEL 1 (
    ECHO [ERROR] Failed to activate virtual environment!
    PAUSE
    EXIT /b 1
)

REM Install and upgrade pip
ECHO [4/7] Installing and upgrading pip...
python -m pip install --upgrade pip

if ERRORLEVEL 1 (
    ECHO [ERROR] Failed to install pip!
    PAUSE
    EXIT /b 1
)

REM Install packages contained in requirements.txt
ECHO [5/7] Installing dependencies from requirements.txt...
pip install -r requirements.txt

if ERRORLEVEL 1 (
    ECHO [ERROR] Failed to install dependencies!
    PAUSE
    EXIT /b 1
)

REM Create output directory
ECHO [6/7] Creating output directory...
IF NOT EXIST output (
    MKDIR output
    ECHO Output directory created
) ELSE (
    ECHO Output directory already exists
)
ECHO.

REM Create .env file if not available
ECHO [7/7] Checking .env file...
IF NOT EXIST .env (
    ECHO Creating .env file...
    (
        ECHO # Environment variables for Data analysis and ML project
        ECHO DATASET_NAME=dataset.csv
        ECHO DATA_DIR=./data
        ECHO OUTPUT_DIR=./output
    ) > .env
    ECHO .env file created successfully
) ELSE (
    ECHO .env file already exists
)
ECHO.

ECHO ========================================
ECHO Setup completed successfully!
ECHO ========================================
ECHO.
ECHO Virtual environment is located at: .venv
ECHO To activate it manually, run: .venv\Scripts\activate.bat
ECHO.

PAUSE
