#!/bin/bash

# Exit immediately if any command fails
set -e

# Install all dependencies from requirements.txt (includes gunicorn if listed)
pip install --no-cache-dir -r requirements.txt

# Install Gramformer directly from GitHub (if not listed in requirements.txt)
pip install git+https://github.com/PrithivirajDamodaran/Gramformer.git

# Install SpaCy language model
python -m spacy download en_core_web_sm

# Debugging: Print installed packages for verification
pip list
