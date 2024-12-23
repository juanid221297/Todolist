#!/bin/bash

# Update and install OpenJDK
apt-get update
apt-get install -y openjdk-11-jdk

# Set JAVA_HOME and add Java to the PATH
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Verify Java installation
java -version

# Proceed with installing Python dependencies
pip install -r requirements.txt
