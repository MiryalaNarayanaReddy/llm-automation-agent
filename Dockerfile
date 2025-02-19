FROM python:3.12-slim-bookworm

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git  # Add Git installation here

# Install UV
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Install Node.js
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Set working directory
WORKDIR /

# Install additional dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Set Git config
RUN git config --global user.email "narayana@gmail.com"
RUN git config --global user.name "narayana"

# Make data directory with write permissions
RUN mkdir -p /data

# Copy application code
COPY . .

# Expose necessary ports
EXPOSE 8000  

# Start the backend server
CMD ["uv", "run", "app.py"]
