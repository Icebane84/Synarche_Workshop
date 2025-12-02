# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install the Graphviz system dependency and clean up apt cache to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends graphviz && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

# Copy the script into the container
COPY visualize_mindmap.py .

# Create a non-root user and switch to it for better security
RUN useradd --create-home appuser
USER appuser

# Set the entrypoint to run the script
ENTRYPOINT ["python", "./visualize_mindmap.py"]