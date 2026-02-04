
FROM python:3.11-slim

# Set working directory to the root of the structure inside the container
WORKDIR /app

# Copy requirements first for cache
COPY backend/requirements.txt /app/backend/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the rest of the application
COPY backend /app/backend
COPY frontend /app/frontend

# Set working directory to where the python app usage expects (inside backend)
WORKDIR /app/backend

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
