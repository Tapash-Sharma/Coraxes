# Use the official Python 2.7 image as the base
FROM python:2.7.18-slim

# Set environment variables to ensure non-interactive installs and UTF-8 locale
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy application files into the container
COPY app.py /app/
COPY coraxes.py /app/
COPY pickle_files/ /app/pickle_files/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version compatible with Python 2.7
RUN python -m pip install --upgrade pip==20.3.4

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask==1.1.4 \
    colorama==0.4.4 \
    beautifulsoup4==4.9.3 \
    IPy==1.1 \
    pandas==0.24.2 \
    scikit-learn==0.20.0 \
    keras==2.0.8 \
    tensorflow==1.5.0 \
    joblib==0.14.1 \
    h5py==2.10.0

# Create the uploads folder
RUN mkdir -p /app/uploads

# Expose the Flask app's port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
