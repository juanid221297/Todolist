#!/bin/bash

# Use the pre-installed Java (if available)
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java installation
java -version || echo "Java not available; skipping Java setup."

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt
