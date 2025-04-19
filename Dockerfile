# Use a lightweight Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Install required system packages (e.g., Java for PySpark)
RUN apt-get update && \
    apt-get install -y default-jdk curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application files into the container
COPY . /app/

# Expose the Flask port (default Flask port is 5000)
EXPOSE 5000

# Run the Flask app using Gunicorn (adjust according to your app structure)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "backend.app:app"]
