# Use an official Python runtime as a parent image
FROM python:3.11.3

# Set the working directory in the container
WORKDIR /app

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    libgomp1

# Copy the current directory contents into the container at /app
COPY .. /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 8080
EXPOSE 8081
EXPOSE 5555

# Extend python path 
RUN export PYTHONPATH=$(pwd):${PYTHONPATH}