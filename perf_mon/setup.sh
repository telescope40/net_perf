#!/usr/bin/env bash
#Install pip
apt install python3-pip -y
# Install virtualenv
pip install virtualenv -y
#Create the Python Virtual Environment
virtualenv .
# Add to
echo 'source ./bin/activate' >> ~/.bashrc
# Activate the python virtual environment
source ./bin/activate
# Create Directory for the project
mkdir -p results/
