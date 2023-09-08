#!/bin/bash

#This script requires root user privileges

# Check if the script is running with sudo privileges
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo or as the root user."
    exit 1
fi
# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3
else
    echo "Python 3 is already installed."
fi

# Check if pip is installed
if ! command -v pip3 &>/dev/null; then
    echo "pip is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
else
    echo "pip is already installed."
fi

# Upgrade pip to the latest version
echo "Upgrading pip to the latest version..."
sudo -H pip3 install --upgrade pip

echo "Python 3 and pip setup complete."

# Install other pre-reqs
echo "installing pandas"
sudo pip install pandas

echo "installing plotly"
sudo pip install plotly.express

echo "All required packages have been installed"


