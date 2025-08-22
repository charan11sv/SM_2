# Use official Python image
FROM python:3.11-slim

# Prevent Python from buffering outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install pip & dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install dependencies (none yet, just pip upgrade)
RUN pip install --upgrade pip

# Copy project files (initially empty, but mount later)
COPY . /app
