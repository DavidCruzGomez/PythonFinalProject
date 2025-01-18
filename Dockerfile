# Use a base Python image
FROM python:3.10

# Project author
LABEL authors="David Cruz Gómez"

# Set the working directory in the container
WORKDIR /app

# Copy only the files needed to install dependencies first
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files to the container
COPY . /app

# Install necessary dependencies for PySide6 and OpenGL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxkbcommon0 \
    libegl1-mesa \
    libdbus-1-3 \
    libxcb-cursor0 \
    libx11-xcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-util1 \
    libxrender1 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Set the PYTHONPATH
ENV PYTHONPATH=/app
ENV QT_QPA_PLATFORM=offscreen

# Expose the port on which the application will run
EXPOSE 8000

# Command to run the application
CMD ["python", "FinalProject/main.py"]
