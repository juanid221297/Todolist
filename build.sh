#!/bin/bash

# Update and install OpenJDK
apt-get update
apt-get install -y openjdk-11-jdk

# Proceed with any other necessary setup, such as installing Python dependencies
pip install -r requirements.txt
