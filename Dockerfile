# 1. Use a lightweight official Python base image
# "slim" versions are smaller and preferred for production
FROM python:3.10-slim

# 2. Prevent Python from writing .pyc files and buffer stdout
# This ensures logs appear immediately in the console
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install system dependencies required for OpenCV
# OpenCV needs these GL libraries to process images (common missing piece in slim images)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Set the working directory inside the container
WORKDIR /app

# 5. Copy requirements first to leverage Docker cache
# This speeds up re-builds if you only change code, not dependencies
COPY requirements.txt .

# 6. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of the application code
COPY . .

# 8. Define the default command to run the app
# We use the new "Senior" version with argparse
ENTRYPOINT ["python", "static_image.py"]