# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . .

# Install dependencies (add your dependencies in a requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "sources/main.py"]