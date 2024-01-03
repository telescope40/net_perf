#!/usr/bin/env bash
# Install virtualenv
pip install virtualenv
#Create the Python Virtual Environment
virtualenv .
# Add to
echo 'source ./bin/activate' >> ~/.bashrc
# Activate the python virtual environment
source ./bin/activate
