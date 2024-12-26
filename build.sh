#!/bin/bash

# Install Docker if not installed
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found, please install it."
    exit
fi

# Build the Docker image
docker build -t grammar-checker .

# Run the Docker container
docker run -p 5000:5000 grammar-checker
