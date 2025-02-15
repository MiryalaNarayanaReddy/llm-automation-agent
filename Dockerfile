FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"


# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR / 

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# make data directory with write permissions
RUN mkdir -p /data

# Copy application code
COPY .  .

# copy audio file to data directory
# COPY ./data/audio.mp3 /data/audio_test.mp3

# Expose necessary ports
EXPOSE 8000  

# Start the backend server

# CMD ["cd","app"]
# CMD ["uv","run","app.py"]

CMD ["uv","run","app.py"]
