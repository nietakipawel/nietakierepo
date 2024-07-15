# Use an appropriate base image
FROM python:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the operator script
COPY operator.py /app/operator.py

# Set the working directory
WORKDIR /app

# Define the command to run the operator
CMD ["kopf", "run", "/app/operator.py"]

