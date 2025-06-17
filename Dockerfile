# Use official Python image with compatible version
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full Django app
COPY . .

# Set default command
CMD ["gunicorn", "backend.backend.wsgi:application", "--bind", "0.0.0.0:8000"]
