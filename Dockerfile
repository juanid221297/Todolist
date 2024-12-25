FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install SpaCy language model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . .

# Expose application port
EXPOSE 5000

# Run the application using Gunicorn
CMD ["gunicorn", "-w", "2", "-t", "300", "-b", "0.0.0.0:5000", "Grammar:app"]
