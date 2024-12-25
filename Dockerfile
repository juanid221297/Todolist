FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
COPY . /app
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Debug gunicorn installation
RUN python --version
RUN pip --version
RUN which gunicorn
RUN gunicorn --version

# Install SpaCy language model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application with Gunicorn

CMD ["python", "-m", "gunicorn", "-w", "2", "-t", "300", "Grammar:app", "-b", "0.0.0.0:5000"]
