# DeMoD EchoForge DSP Schematic Processing Container

**Current Version:** 1.0.0  
**Last Updated:** 2025-10-12  
**Author:** ALH477  
**License:** CERN-OHL-S v2

## Overview

Docker container environment for processing DSP audio interface schematics using skidl and kinet2pcb. Specifically designed for the TMS320C6657 DSP-based audio processing system with DDR3 memory integration and stereo audio I/O.

## Prerequisites

- Docker 25.0.0 or higher
- 2GB free disk space
- Git
- Internet connection for pulling dependencies

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ALH477/DeMoD-EchoForge-DSP.git
cd DeMoD-EchoForge-DSP

# Make run script executable
chmod +x run.sh

# Run the container
./run.sh
```

## Directory Structure

```
DeMoD-EchoForge-DSP/
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
├── run.sh              # Execution script
├── schematic.py        # Main schematic processing script
├── init_env.py         # Environment initialization
├── output/             # Generated schematics
├── libraries/          # Custom KiCad libraries
└── logs/              # Processing logs
```

## Container Details

### Base Image
- Ubuntu 24.04 LTS
- Python 3.11
- KiCad Latest Stable

### Key Components
- skidl (Latest from source)
- kinet2pcb (Latest from source)
- KiCad Libraries
- Cairo Graphics
- GTK Support

### Environment Variables
```bash
KISYSMOD=/usr/share/kicad/modules
KICAD_SYMBOL_DIR=/usr/share/kicad/library
PYTHONPATH=/opt/venv/lib/python3.11/site-packages
TZ=UTC
```

## Usage

### Basic Execution
```bash
./run.sh
```

### Custom Library Integration
Place custom KiCad libraries in the `libraries/` directory before running:
```bash
cp your-custom-lib.lib libraries/
./run.sh
```

### Output Files
Generated files are placed in the `output/` directory:
- `production_dsp_schematic.kicad_sch`: Main schematic file
- Run logs with timestamp (format: `run_YYYYMMDD_HHMMSS.log`)

## Volumes

The container uses three mounted volumes:
1. `/app/output`: Generated schematic files
2. `/app/libraries`: Custom KiCad libraries
3. `/app/logs`: Processing logs

## Error Handling

Logs are generated for each run with UTC timestamps. Check the `logs/` directory for detailed execution information.

Example log entry:
```
[2025-10-12 12:46:22 UTC] Starting schematic generation
[2025-10-12 12:46:23 UTC] Environment initialized
[2025-10-12 12:46:25 UTC] Schematic generated successfully
```

## Building from Source

```bash
# Clone repository
git clone https://github.com/ALH477/DeMoD-EchoForge-DSP.git

# Build container
cd DeMoD-EchoForge-DSP
docker build -t dsp-schematic:latest .

# Run with custom name
docker run --name my-dsp-schematic \
    -v "$(pwd)/output:/app/output" \
    -v "$(pwd)/libraries:/app/libraries" \
    -v "$(pwd)/logs:/app/logs" \
    dsp-schematic:latest
```

## Development

### Adding Custom Components
1. Place custom library files in `libraries/`
2. Update `init_env.py` if needed
3. Rebuild container

### Debugging
```bash
# Run container interactively
docker run -it --entrypoint /bin/bash dsp-schematic:latest

# Test environment
python3 /app/init_env.py
```

## Known Issues

- Large schematics may require increased Docker memory allocation
- Some KiCad symbols may need manual library path configuration

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under CERN Open Hardware Licence Strongly Reciprocal (CERN-OHL-S) v2.
See LICENSE file in repository root for full terms.

## Support

For issues and support:
- Create an issue in the GitHub repository
- Contact: [GitHub Issues](https://github.com/ALH477/DeMoD-EchoForge-DSP/issues)

## Acknowledgments

- xesscorp for skidl and kinet2pcb
- KiCad team for the excellent EDA suite
- Ubuntu team for the stable base system

## Version History

- 1.0.0 (2025-10-12)
  - Initial release
  - Basic schematic processing support
  - Full KiCad integration
  - Logging system implementation