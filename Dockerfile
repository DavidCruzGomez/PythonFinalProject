# Use a base Python image with compatible Debian version
FROM python:3.10-slim

# Project author
LABEL authors="David Cruz Gómez"

# Set environment variables for Qt
ENV QT_QPA_PLATFORM="xcb"
ENV QT_DEBUG_PLUGINS=1
ENV DISPLAY=":0"
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV XCURSOR_PATH=/usr/share/icons
ENV XCURSOR_THEME=DMZ-White
ENV PYTHONPATH=/app

# Install system dependencies first for better caching
RUN apt-get update && apt-get install -y --no-install-recommends \
    xauth \
    xvfb \
    libx11-xcb1 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxcb1 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    libdbus-1-3 \
    libglib2.0-0 \
    libegl1 \
    libgl1 \
    libgles2 \
    libglx0 \
    libxcomposite1 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libxrender1 \
    libxshmfence1 \
    libxxf86vm1 \
    libwayland-client0 \
    libwayland-server0 \
    mesa-utils \
    qtwayland5 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the port on which the application will run
EXPOSE 8000

# Run application with Xvfb and debug logging
CMD Xvfb :0 -screen 0 1024x768x24 -ac +extension GLX +render -noreset & \
    sleep 2 && \
    python FinalProject/main.py
