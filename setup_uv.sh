#!/bin/bash

# ============================================
# UV-based Virtual Environment Setup Script
# ============================================
# This script creates a Python virtual environment using UV
# and installs all required dependencies.
#
# Prerequisites: UV must be installed
# Install UV: https://github.com/astral-sh/uv
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
echo "UV Virtual Environment Setup"
echo "========================================"
echo ""

# Check if UV is installed
echo -e "${BLUE}[1/6]${NC} Checking if UV is installed..."
if ! command -v uv &> /dev/null; then
    echo ""
    echo -e "${RED}[ERROR]${NC} UV is not installed or not in PATH!"
    echo ""
    echo "Please install UV first:"
    echo "  - Linux/Mac: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  - Or visit: https://github.com/astral-sh/uv"
    echo ""
    exit 1
fi

# Display UV version
UV_VERSION=$(uv --version 2>&1)
echo -e "${GREEN}UV detected:${NC} $UV_VERSION"
echo ""

# Create virtual environment using UV
echo -e "${BLUE}[2/6]${NC} Creating virtual environment with UV..."
if uv venv .venv; then
    echo -e "${GREEN}Virtual environment created successfully${NC}"
else
    echo -e "${RED}[ERROR]${NC} Failed to create virtual environment!"
    exit 1
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}[3/6]${NC} Activating virtual environment..."
source .venv/bin/activate

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Virtual environment activated${NC}"
else
    echo -e "${RED}[ERROR]${NC} Failed to activate virtual environment!"
    exit 1
fi
echo ""

# Install dependencies using UV
echo -e "${BLUE}[4/6]${NC} Installing dependencies from requirements.txt..."
if uv pip install -r requirements.txt; then
    echo -e "${GREEN}Dependencies installed successfully${NC}"
else
    echo -e "${RED}[ERROR]${NC} Failed to install dependencies!"
    exit 1
fi
echo ""

# Create output directory
echo -e "${BLUE}[5/6]${NC} Creating output directory..."
if [ ! -d "output" ]; then
    mkdir output
    echo -e "${GREEN}Output directory created${NC}"
else
    echo -e "${YELLOW}Output directory already exists${NC}"
fi
echo ""

# Create .env file if not available
echo -e "${BLUE}[6/6]${NC} Checking .env file..."
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