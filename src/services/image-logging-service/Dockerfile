# Stage 1: Build stage
FROM python:3.12-slim AS builder

# Set environment variables to prevent Python from buffering output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies into a custom directory
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-slim

# Set environment variables to prevent Python from buffering output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxrender1 \
    libxext6 \
    libsm6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install runtime system dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    libgl1-mesa-glx libglib2.0-0 libxrender1 libxext6 libsm6 && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

# Set the working directory in the production image
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /app/dependencies /usr/local/lib/python3.12/site-packages

# Copy the application code
COPY src/ .

COPY temp/libs ./libs

# Установить PYTHONPATH
ENV PYTHONPATH="/app/libs"

# Define the default command
CMD ["python", "main.py"]