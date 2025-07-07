# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend files
COPY app/ ./app/
COPY requirements.txt ./app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r ./app/requirements.txt

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]
