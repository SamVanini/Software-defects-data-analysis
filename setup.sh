#!/bin/bash

# Check if python is installed
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3.9 or higher required."
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Python version $python_version is less than required version $required_version"
    exit 1
fi

# Check if python3-venv is installed
echo "Python detected correctly, proceeding with python3-venv installation check..."

if ! dpkg --get-selections | grep -q "^python3-venv[[:space:]]*install$"; then
    echo "python3-venv is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python$python_version-venv
else
    echo "python$python_version-venv is already installed."
fi

# Create python local environment
echo "python3-venv detected correctly, proceeding with .venv creation..."
python3 -m venv env

# Activate local pyton env
echo "Activating virtual environment..."
source env/bin/activate

# Install and upgrade pip
echo "Installing and upgrading pip..."
env/bin/pip  install --upgrade pip

# Install packages contained in requi#ents.txt
echo "Installing dependencies..."
env/bin/pip install -r requirements.txt

# Create output dir
echo Creating output directory...
mkdir -p output

# Create env file if not available
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Environment variables for Data analysis and ML project
DATASET_NAME=TBD
DATA_DIR=./data
OUTPUT_DIR=./output
EOF
    echo ".env file successfully created !"
fi