#!/bin/bash

# Use the pre-installed Java (if available)
pip install git+https://github.com/PrithivirajDamodaran/Gramformer.git
# Install Python dependencies
pip install --no-cache-dir -r requirements.txt
python -m spacy download en_core_web_sm

