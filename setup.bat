@ECHO OFF
REM Check if python is installed
REM The command is used to check if Python is installed and available in the system's environment without displaying any output.
REM Standard output and error are redirected to null

ECHO Checking Python version...

python --version >nul 2>&1

if ERRORLEVEL 1 (
    ECHO Python 3.9 or higher required.
    PAUSE
    EXIT /b 1
)

REM Create python local environment
ECHO Python detected correctly, proceeding with .venv creation...
python -m venv env

REM Activate local pyton env
ECHO Activating virtual environment...
CALL env\Scripts\activate.bat

REM Install and upgrade pip
ECHO Installing and upgrading pip...
python -m pip install --upgrade pip

REM Install packages contained in requirements.txt
ECHO Installing dependencies...
pip install -r requirements.txt

REM Create output folder, if not available
ECHO Creating output directory...
IF NOT EXIST output MKDIR output

REM Create env file if not available
IF NOT EXIST .env (
    ECHO Creating .env file...
    (
        ECHO # Environment variables for Data analysis and ML project
        ECHO DATASET_NAME=TBD
        ECHO DATA_DIR=./data
        ECHO OUTPUT_DIR=./output
    ) > .env
    ECHO .env file successfully created !
)

PAUSE
