#!/bin/bash

# ============================================
# Python-based Virtual Environment Setup Script
# ============================================
# This script creates a Python virtual environment using
# venv and installs all required dependencies.
#
# Prerequisites: Python must be installed
# Install Python: http://python.org/downloads/
# ============================================

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "========================================"
echo "Python Virtual Environment Setup"
echo "========================================"
echo ""

# Check if python is installed
echo -e "${BLUE}[1/7]${NC} Checking if Python is installed..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo -e "${RED}[ERROR]${NC} Python is not installed or not in PATH!"
    echo ""
    echo "Please install Python first:"
    echo "  - Visit: http://python.org/downloads/"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}[ERROR]${NC} Python version $PYTHON_VERSION is less than required version $REQUIRED_VERSION"
    exit 1
fi

echo -e "${GREEN}Python detected:${NC} $PYTHON_VERSION"
echo ""

# Check if python3-venv is installed
echo -e "${BLUE}[2/7]${NC} Proceeding with python$PYTHON_VERSION-venv installation check..."

if ! dpkg --get-selections | grep -q "^python3-venv[[:space:]]*install$"; then
    echo -e "${YELLOW}python$PYTHON_VERSION-venv is not installed. Installing...${NC}"
    sudo apt-get update
    sudo apt-get install -y python$PYTHON_VERSION-venv
    echo -e "${GREEN}python$PYTHON_VERSION-venv detected correctly${NC}"
else
    echo -e "${YELLOW}python$PYTHON_VERSION-venv is already installed.${NC}"
fi
echo ""

# Create python local environment
echo ", proceeding with .venv creation..."
if python3 -m venv env; then
    echo -e "${GREEN}Virtual environment created successfully${NC}"
else
    echo -e "${RED}[ERROR]${NC} Failed to create virtual environment!"
    exit 1
fi
echo ""

# Activate local pyton env
echo -e "${BLUE}[3/7]${NC} Activating virtual environment..."
source env/bin/activate

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Virtual environment activated${NC}"
else
    echo -e "${RED}[ERROR]${NC} Failed to activate virtual environment!"
    exit 1
fi
echo ""

# Install and upgrade pip
echo -e "${BLUE}[4/7]${NC} Installing and upgrading pip..."
if env/bin/pip  install --upgrade pip; then
    echo -e "${GREEN}Pip installed successfully${NC}"
else
    echo -e "${RED}[ERROR]${NC} Failed to install pip!"
    exit 1
fi
echo ""

# Install packages contained in requi#ents.txt
echo -e "${BLUE}[5/7]${NC} Installing dependencies from requirements.txt..."
if env/bin/pip install -r requirements.txt; then
    echo -e "${GREEN}Dependencies installed successfully${NC}"
else
    echo -e "${RED}[ERROR]${NC} Failed to install dependencies!"
    exit 1
fi
echo ""

# Create output directory
echo -e "${BLUE}[6/7]${NC} Creating output directory..."
if [ ! -d "output" ]; then
    mkdir output
    echo -e "${GREEN}Output directory created${NC}"
else
    echo -e "${YELLOW}Output directory already exists${NC}"
fi
echo ""

# Create .env file if not available
echo -e "${BLUE}[7/7]${NC} Checking .env file..."
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << 'EOF'
# Environment variables for Data analysis and ML project
DATASET_NAME=dataset.csv
DATA_DIR=./data
OUTPUT_DIR=./output
EOF
    echo -e "${GREEN}.env file created successfully${NC}"
else
    echo -e "${YELLOW}.env file already exists${NC}"
fi
echo ""

echo "========================================"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo "========================================"
echo ""
echo "Virtual environment is located at: .venv"
echo "To activate it manually, run: source .venv/bin/activate"
echo ""