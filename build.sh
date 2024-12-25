#!/bin/bash

# Exit immediately if any command fails
set -e

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Install SpaCy language model
python -m spacy download en_core_web_sm

# Debugging: Print installed packages for verification
pip list
