#!/bin/bash

# Configuration
CONTAINER_NAME="dsp-schematic-env"
IMAGE_NAME="dsp-schematic:latest"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create required directories
mkdir -p output libraries logs

echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t $IMAGE_NAME .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Build successful${NC}"
    
    echo -e "${YELLOW}Running container...${NC}"
    docker run \
        --name "${CONTAINER_NAME}_${TIMESTAMP}" \
        -v "$(pwd)/output:/app/output" \
        -v "$(pwd)/libraries:/app/libraries" \
        -v "$(pwd)/logs:/app/logs" \
        -e "USER_LOGIN=ALH477" \
        -e "TZ=UTC" \
        $IMAGE_NAME

    # Check container exit status
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Processing completed successfully${NC}"
        echo "Output files are in the ./output directory"
        echo "Logs are in the ./logs directory"
    else
        echo -e "${RED}Processing failed${NC}"
        echo "Check logs in ./logs directory for details"
    fi
else
    echo -e "${RED}Build failed${NC}"
fi
