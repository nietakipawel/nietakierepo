# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Kopf framework
RUN pip install kopf

# Run the operator.py script when the container launches
CMD ["kopf", "run", "/app/operator.py"]
