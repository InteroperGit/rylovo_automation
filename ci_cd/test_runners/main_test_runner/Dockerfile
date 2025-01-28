FROM python:3.9-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

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

# Устанавливаем Docker Compose (если нужно для тестов)
RUN apt-get update && apt-get install -y docker-compose

# Устанавливаем pytest
RUN pip install pytest

CMD ["pytest", "-v"]