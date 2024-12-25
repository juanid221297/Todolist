FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn==20.1.0  # Ensure gunicorn is installed

# Debugging step
RUN gunicorn --version
RUN ls -la /app

# Install SpaCy language model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application with Gunicorn
CMD ["gunicorn", "-w", "2", "-t", "120", "Grammar:app", "-b", "0.0.0.0:5000"]
