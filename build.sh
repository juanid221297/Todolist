#!/bin/bash

# Update and install only the required dependencies
apt-get update
apt-get install -y openjdk-11-jdk  # Required for language_tool_python

# Set JAVA_HOME and add Java to the PATH
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java installation
java -version

# Proceed with installing Python dependencies
pip install --no-cache-dir -r requirements.txt
