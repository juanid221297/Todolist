# Use a Python 3.11 base image
FROM python:3.11-slim

# Install Java (OpenJDK 11)
RUN apt-get update && apt-get install -y openjdk-11-jre-headless

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that your app will run on
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "Grammar:app", "-b", "0.0.0.0:5000"]
