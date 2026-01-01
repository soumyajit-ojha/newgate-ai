# Python Backend 
FROM python:3.12-slim

# Set a common project root
WORKDIR /project_root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder to /project_root/backend
COPY backend/ ./backend/

# We switch into 'backend' directory so uvicorn runs 'app.main' correctly
WORKDIR /project_root/backend

ENV PYTHONPATH=/project_root/backend
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Start Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
