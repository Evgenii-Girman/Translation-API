# Use the latest official Python slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for API access (use default or overridden value)
EXPOSE ${PORT:-8000}

# Command to run the application using environment variables
CMD ["sh", "-c", "uvicorn src.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]
