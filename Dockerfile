# Use Ubuntu 24.04 LTS (Latest LTS as of 2025)
FROM ubuntu:24.04

# Set metadata
LABEL maintainer="ALH477"
LABEL version="1.0"
LABEL description="DSP Schematic Generation Environment"
LABEL created="2025-10-12"

# Prevent timezone prompt during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3-venv \
    python3-dev \
    kicad \
    git \
    build-essential \
    libcairo2-dev \
    pkg-config \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    libgirepository1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install build tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install skidl and kinet2pcb from source
RUN git clone https://github.com/xesscorp/skidl.git /tmp/skidl && \
    cd /tmp/skidl && \
    python setup.py install && \
    cd /app && \
    rm -rf /tmp/skidl

RUN git clone https://github.com/xesscorp/kinet2pcb.git /tmp/kinet2pcb && \
    cd /tmp/kinet2pcb && \
    python setup.py install && \
    cd /app && \
    rm -rf /tmp/kinet2pcb

# Set up KiCad environment
ENV KISYSMOD=/usr/share/kicad/modules
ENV KICAD_SYMBOL_DIR=/usr/share/kicad/library
ENV PYTHONPATH="${PYTHONPATH}:/opt/venv/lib/python3.11/site-packages"

# Create necessary directories
RUN mkdir -p /app/output /app/libraries /app/logs

# Copy application files
COPY schematic.py /app/
COPY init_env.py /app/

# Create initialization script
RUN echo '#!/bin/bash\n\
timestamp=$(date +"%Y%m%d_%H%M%S")\n\
log_file="/app/logs/run_$timestamp.log"\n\
\n\
echo "[$(date -u "+%Y-%m-%d %H:%M:%S UTC")] Starting schematic generation" | tee -a "$log_file"\n\
\n\
# Initialize environment\n\
source /opt/venv/bin/activate\n\
\n\
# Run schematic script\n\
python schematic.py 2>&1 | tee -a "$log_file"\n\
\n\
# Check for output file\n\
if [ -f "production_dsp_schematic.kicad_sch" ]; then\n\
    echo "[$(date -u "+%Y-%m-%d %H:%M:%S UTC")] Schematic generated successfully" | tee -a "$log_file"\n\
    cp production_dsp_schematic.kicad_sch /app/output/\n\
    cp "$log_file" /app/output/\n\
else\n\
    echo "[$(date -u "+%Y-%m-%d %H:%M:%S UTC")] Error: Schematic generation failed" | tee -a "$log_file"\n\
    exit 1\n\
fi' > /app/run.sh && chmod +x /app/run.sh

# Create environment initialization script
RUN echo 'import os\n\
import sys\n\
import datetime\n\
import skidl\n\
import kinet2pcb\n\
\n\
def init_environment():\n\
    """Initialize the development environment"""\n\
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")\n\
    print(f"[{timestamp}] Initializing environment...")\n\
    \n\
    try:\n\
        skidl.reset()\n\
        skidl.lib_search_paths[skidl.KICAD] = [\n\
            "/usr/share/kicad/library",\n\
            "/app/libraries"\n\
        ]\n\
        return True\n\
    except Exception as e:\n\
        print(f"[{timestamp}] Error: {e}")\n\
        return False\n\
\n\
if __name__ == "__main__":\n\
    if init_environment():\n\
        print("Environment initialized successfully")\n\
        sys.exit(0)\n\
    else:\n\
        print("Environment initialization failed")\n\
        sys.exit(1)\n\
' > /app/init_env.py

# Set permissions
RUN chmod -R 755 /app

# Create volume for output and libraries
VOLUME ["/app/output", "/app/libraries", "/app/logs"]

# Set the entrypoint
ENTRYPOINT ["/app/run.sh"]
