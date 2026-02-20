@ECHO OFF
REM ============================================
REM UV-based Virtual Environment Setup Script
REM ============================================
REM This script creates a Python virtual environment using UV
REM and installs all required dependencies.
REM
REM Prerequisites: UV must be installed
REM Install UV: https://github.com/astral-sh/uv
REM ============================================

ECHO.
ECHO ========================================
ECHO UV Virtual Environment Setup
ECHO ========================================
ECHO.

REM Check if UV is installed
ECHO [1/6] Checking if UV is installed...
uv --version >nul 2>&1

if ERRORLEVEL 1 (
    ECHO.
    ECHO [ERROR] UV is not installed or not in PATH!
    ECHO.
    ECHO Please install UV first:
    ECHO   - Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ECHO   - Or visit: https://github.com/astral-sh/uv
    ECHO.
    PAUSE
    EXIT /b 1
)

REM Display UV version
FOR /F "tokens=*" %%i IN ('uv --version 2^>^&1') DO SET UV_VERSION=%%i
ECHO UV detected: %UV_VERSION%
ECHO.

REM Create virtual environment using UV
ECHO [2/6] Creating virtual environment with UV...
uv venv .venv

if ERRORLEVEL 1 (
    ECHO [ERROR] Failed to create virtual environment!
    PAUSE
    EXIT /b 1
)

ECHO Virtual environment created successfully
ECHO.

REM Activate virtual environment
ECHO [3/6] Activating virtual environment...
CALL .venv\Scripts\activate.bat

if ERRORLEVEL 1 (
    ECHO [ERROR] Failed to activate virtual environment!
    PAUSE
    EXIT /b 1
)

ECHO Virtual environment activated
ECHO.

REM Install dependencies using UV
ECHO [4/6] Installing dependencies from requirements.txt...
uv pip install -r requirements.txt

if ERRORLEVEL 1 (
    ECHO [ERROR] Failed to install dependencies!
    PAUSE
    EXIT /b 1
)

ECHO Dependencies installed successfully
ECHO.

REM Create output directory
ECHO [5/6] Creating output directory...
IF NOT EXIST output (
    MKDIR output
    ECHO Output directory created
) ELSE (
    ECHO Output directory already exists
)
ECHO.

REM Create .env file if not available
ECHO [6/6] Checking .env file...
IF NOT EXIST .env (
    ECHO Creating .env file...
    (
        ECHO # Environment variables for Data analysis and ML project
        ECHO DATASET_NAME=TBD
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