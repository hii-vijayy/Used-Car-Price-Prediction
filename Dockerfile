FROM python:3.11-bullseye

# Install Java using apt (safer than manual download)
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-11-jdk-headless && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Python env setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Spark config
ENV SPARK_DRIVER_MEMORY=2g
ENV SPARK_EXECUTOR_MEMORY=2g
ENV SPARK_LOCAL_DIRS=/tmp/spark

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--timeout", "300", "--workers", "1", "backend.app:app"]
