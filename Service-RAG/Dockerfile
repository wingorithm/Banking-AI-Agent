# Use a base image with Python and GPU support
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application and supporting files
COPY . /app/

# Expose the FastAPI port
EXPOSE 8000

# Expose the Ollama port (internal use within Docker)
EXPOSE 11434

# Install Ollama's server binary
RUN curl -L https://ollama.com/download/server -o /usr/local/bin/ollama && chmod +x /usr/local/bin/ollama

# Entry point to start both services
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
