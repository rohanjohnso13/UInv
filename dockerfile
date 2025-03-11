# Use Python 3.9 base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask to run on
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
