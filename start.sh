# !/bin/bash

# BACKEND: CHECK FOR VENV AND CREATE ONE AND INSTALL LIBRARIES IF NOT FOUND

# Directory containing the virtual environment
VENV_DIR="./backend/bird_venv"

# Check if the directory exists and contains a virtual environment
if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
    echo "Virtual environment already exists in $VENV_DIR."
else
    echo "Virtual environment not found. Creating one in $VENV_DIR..."
    
    # Navigate to the backend directory
    if [ ! -d "./backend" ]; then
        echo "Error: ./backend directory does not exist."
        exit 1
    fi

    # Create the virtual environment
    python3 -m venv ./backend/bird_venv

    if [ $? -eq 0 ]; then
        echo "Virtual environment successfully created in $VENV_DIR."
    else
        echo "Failed to create virtual environment. Ensure Python 3 and venv are installed."
        exit 1
    fi
fi

if [ -f "./backend/requirements.txt" ]; then
    # Enter the virtual environment
    source ./backend/bird_venv/bin/activate
    # install dependencies
    pip install --upgrade pip
    pip install -r "./backend/requirements.txt"
    echo "Installing dependencies..."
else
    echo "requirements.txt not found. Do you have the latest repo version from Github?"
    exit 1
fi

# FRONTEND: CHECK FOR NPM AND DEPENDENCIES

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Installing npm..."
    
    # Install npm (assumes Node.js is available in system package manager)
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y nodejs npm
    elif command -v yum &> /dev/null; then
        sudo yum install -y nodejs npm
    elif command -v brew &> /dev/null; then
        brew install node
    else
        echo "Could not determine package manager. Please install npm manually."
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        echo "npm installation failed. Please check your setup and try again."
        exit 1
    fi
else
    echo "npm is already installed."
fi

# Check for the ./frontend directory
FRONTEND_DIR="./frontend"

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "Error: $FRONTEND_DIR directory does not exist."
    exit 1
fi

# Navigate to the frontend directory
cd "$FRONTEND_DIR"
echo "$FRONTEND_DIR"

# Check for package.json file
if [ ! -f "package.json" ]; then
    echo "Error: package.json file not found in $FRONTEND_DIR."
    exit 1
fi

# Install npm dependencies
echo "Installing dependencies from ./frontend/package.json..."
npm install

if [ $? -eq 0 ]; then
    echo "Dependencies successfully installed."
else
    echo "Failed to install dependencies. Please check your package.json or npm setup."
    exit 1
fi

source ../backend/bird_venv/bin/activate