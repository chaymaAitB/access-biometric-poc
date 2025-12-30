# Backend
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# libgl1-mesa-glx for OpenCV
# build-essential for compiling some python packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
