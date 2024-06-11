# Set python version
ARG BASE_CONTAINER=python:3.8

# Set the base image 
FROM --platform=linux/amd64 $BASE_CONTAINER

# Set working directory
WORKDIR /extraction-app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure .env is in the correct location (if needed)
# COPY ../.env ./.env  # Uncomment this line if your .env file is in the parent directory of your Dockerfile

# Set the entry point to execute the application
CMD ["python", "-m", "app"]
