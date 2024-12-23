#!/bin/bash

# Update package lists
apt-get update -y

# Install Python dependencies
pip install -r requirements.txt
pip install git+https://github.com/PrithivirajDamodaran/Gramformer.git
# Verify successful installation
python -m pip show gramformer

# Print message indicating setup is complete
echo "Setup complete. Dependencies installed."
