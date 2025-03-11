# Use Python 3.9 base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies (if any, like tkinter or csv, you can add them to requirements.txt if needed)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on (if applicable)
EXPOSE 5000

# Command to run your app
CMD ["python", "app.py"]
