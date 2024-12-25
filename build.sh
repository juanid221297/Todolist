#!/bin/bash

# Install Gramformer directly from GitHub
pip install git+https://github.com/PrithivirajDamodaran/Gramformer.git

# Install SpaCy language model
python -m spacy download en_core_web_sm
