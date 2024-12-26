# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies using Poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev --no-interaction

# Copy the rest of the application files
COPY . /app/

# Expose the application port
EXPOSE 5000

# Start the Flask app with gunicorn for production
CMD ["poetry", "run", "gunicorn", "-w", "2", "-t", "300", "Grammar:app", "-b", "0.0.0.0:5000"]
