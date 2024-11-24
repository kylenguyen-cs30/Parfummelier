# Use Python 3.9 slim image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        libpq-dev \
        python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Clean install dependencies
RUN pip uninstall -y motor pymongo && \
    pip install --no-cache-dir -r requirements.txt



# Create uploads directory 
RUN mkdir -p /app/uploads/images \
    && chmod 777 /app/uploads/images


# Copy the rest of the application
COPY . .


# Expose the port
EXPOSE 5000

# Start the FastAPI application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
