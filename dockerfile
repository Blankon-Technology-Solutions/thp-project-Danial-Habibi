# Use an official Python runtime as a parent image
FROM python:3.6.2-alpine

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk update && \
    apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    && rm -rf /var/cache/apk/*

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
