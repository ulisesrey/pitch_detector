# 1. Base Image: Use a stable, lightweight Python image
FROM python:3.12-slim

# 2. System Dependencies: Install FFmpeg
# FFmpeg is essential for librosa to resolve the 'NoBackendError'.
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    # Clean up to keep the image size small
    rm -rf /var/lib/apt/lists/*

# 3. Working Directory: Set the context for subsequent commands
WORKDIR /usr/src/app

# 4. Install uv: We need uv to read the lock file
RUN pip install --no-cache-dir uv

# 5. Application Dependencies: Copy files and sync dependencies
# We copy pyproject.toml and uv.lock as these define the environment
COPY pyproject.toml .
COPY uv.lock .

# Use 'uv sync' to install all dependencies exactly as specified in uv.lock
RUN uv sync

# 6. Application Code: Copy the rest of the project files
COPY . .

# 7. Entrypoint: Command to run the application using Gunicorn
CMD [".venv/bin/python", "-m", "gunicorn", "--bind", "0.0.0.0:$PORT", "src.pitch_detector.app:app"]