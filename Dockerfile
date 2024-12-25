# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Install system dependencies (Java for Gramformer and others)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install SpaCy's English language model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your application code into the container
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Ensure gunicorn is in PATH and run the app
CMD ["gunicorn", "Grammar:app", "-b", "0.0.0.0:5000", "-w", "2", "-t", "120"]
