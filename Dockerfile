# Use slim Python for small image size
FROM python:3.10-slim

# Set work directory inside the container
WORKDIR /app

# Install system dependencies (if needed later)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for Docker caching)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY src/ /app/src/
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY assets/ /app/assets/
COPY src/model_go.pkl /app/src/model_go.pkl
COPY src/model_fg.pkl /app/src/model_fg.pkl
COPY src/model_punt.pkl /app/src/model_punt.pkl

# Provide a default environment variable for port
ENV PORT=8080

# Expose Flask port
EXPOSE 8080

# Run the Flask app
CMD ["python", "src/app.py"]
