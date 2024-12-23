# Use the official Python base image
FROM python:3.11-slim

# Install OpenJDK
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your application will run on
EXPOSE 5000

# Command to run your application
CMD ["gunicorn", "Grammar:app"]
