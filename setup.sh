#!/bin/bash


# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv
sudo apt install -y wget unzip

# Install tools



# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install python dependencies
pip install -r requirements.txt

# Install Seclist dependencies

sudo rm -rf /usr/share/seclists && sudo wget https://github.com/danielmiessler/SecLists/archive/refs/tags/2025.1.zip -O /usr/share/SecLists.zip
sudo unzip /usr/share/SecLists.zip -d /usr/share/ 
sudo mv /usr/share/SecLists-2025.1 /usr/share/seclists
sudo rm /usr/share/SecLists.zip
