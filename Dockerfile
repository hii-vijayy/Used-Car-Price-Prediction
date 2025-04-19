# Use official Python image
FROM python:3.11-slim

# Install Java (required for PySpark)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set the working directory inside the container
WORKDIR /app

# Copy backend files into the container
COPY ./backend /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the app using gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5001"]
