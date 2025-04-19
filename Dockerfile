FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Java 17 and other required packages
RUN apt-get update && \
    apt-get install -y default-jdk procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME properly using the update-alternatives system
RUN JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::") && \
    echo "export JAVA_HOME=$JAVA_HOME" >> /etc/profile && \
    echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment

# Load JAVA_HOME from the environment file
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="$JAVA_HOME/bin:$PATH"


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
EXPOSE 5001

# Run the Flask app using Gunicorn (adjust according to your app structure)
CMD ["gunicorn", "--bind", "0.0.0.0:5001","--timeout", "120", "--workers", "1", "backend.app:app"]
