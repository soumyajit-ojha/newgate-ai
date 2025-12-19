# ---------------------------------------
# STAGE 1: Build Frontend
# ---------------------------------------
FROM node:20-alpine AS frontend-builder

# equal to cd /app/frontend
WORKDIR /app/frontend

# Copy package.json and lock file
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ ./

# Build Arguments (Ensure VITE_API_URL matches your backend prefix, usually /api)
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL

# Set ENV so the build process can see them
ARG VITE_GOOGLE_CLIENT_ID
ENV VITE_GOOGLE_CLIENT_ID=$VITE_GOOGLE_CLIENT_ID

# Build! (Creates /app/frontend/dist)
RUN npm run build


# ---------------------------------------
# STAGE 2: Python Backend (The fix is here)
# ---------------------------------------
FROM python:3.12-slim

# 1. Set a common project root
WORKDIR /project_root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Setup Backend
# Copy requirements first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder to /project_root/backend
COPY backend/ ./backend/

# 3. Setup Frontend (Crucial Step)
# Copy the built 'dist' folder to /project_root/frontend/dist
# This ensures "parent.parent.parent / frontend / dist" finds this folder
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# 4. Run Configuration
# We switch into 'backend' directory so uvicorn runs 'app.main' correctly
WORKDIR /project_root/backend

ENV PYTHONPATH=/project_root/backend
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Start Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
