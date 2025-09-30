# USB-C DSP Audio Interface

Being opinionated about your tools, the entities that exist solely to provide a means to an end. Is not a lost cause for many reasons, they are the conduit of your creativity. There are many artisans in history and modern times who make their own tools. The best example of this is the Blacksmith.
They build each tool they need for their unique desires. Specifically forged for their art, which may even be the tool itself. My point is that each variable in your cocktail of creation will define the result of a fine imprint that creates its character and soul. So continue to be an opinionated ass, its your obligation as a creator. Make your own tools if needed, but there is no shame in using what others have built.
This can actually lead to improvements on these legacy FOSS applications. The beauty of FOSS or OSS is that you can modify it to your needs. My goals with DeMoD have been this from the beginning, giving the creator the tools to build what they need. A lot of my work appears tangential and scatterbrained, if you consider everything I have done in detail. It all connects to itself, constantly referring to itself for a self fulfilling ecosystem.
My love for Open Source has inspired my business model, I plan to create many Open Sources solutions for many use cases.
Every artist deserves to make their tool a work of art. People like Les Paul, Terry Davis, and Van Halen understood this as well. Those are the first few that come to mind but there are many more examples. There is a reason why every good luthier takes great pride in what they do.
Be opinionated, it defines who you are and how you create. If you cannot find your needs, then make them, obsess over the necessary tools for the job. This is how invention comes to fruition.

## Overview

This repository contains the open-source hardware design for a compact USB-C powered digital signal processor (DSP) audio interface. The device is centered on the Texas Instruments TMS320C6657 DSP, supported by 8Gb DDR3L RAM for high-bandwidth data processing, the TI TAC5212 stereo audio codec for high-fidelity conversion, and a USB-C port for data transfer and power. It offers stereo audio input and output via 3.5mm TRS jacks, enabling real-time audio applications with low latency and high performance.

The design emphasizes signal integrity and noise reduction through separated digital (DGND) and analog (AGND) grounds with star grounding, comprehensive decoupling, and a 4-layer PCB layout. Production features include ESD protection on USB and audio ports, a resettable fuse on VBUS, a power LED, a JTAG debugging header, and ZQ calibration resistors for DDR3 reliability.

This project is licensed under the CERN Open Hardware Licence Strongly Reciprocal (CERN-OHL-S) v2. Copyright © 2025 DeMoD LLC and Asher LeRoy. All rights reserved under the terms of the license. Derivatives must remain open and credit the original copyright holders.

## Features

- **DSP Processing**: Dual-core C66x DSP (TMS320C6657) up to 1.25 GHz for advanced real-time algorithms such as filtering, effects, or AI-driven audio enhancement.
- **Memory**: 1GB DDR3L SDRAM with full x16 interface for large data buffers in applications like reverb or spectral analysis.
- **Audio Codec**: TAC5212 with high dynamic range ADC/DAC supporting up to 192 kHz/32-bit stereo in I2S/TDM formats.
- **USB Interface**: USB-C receptacle with USB 2.0 OTG support for audio streaming and control, including CC pull-downs for device mode.
- **Audio I/O**: Dual 3.5mm TRS jacks for stereo input (e.g., instruments/microphones) and output (e.g., headphones/speakers), with low-pass filtering on one channel.
- **Power Management**: Dual low-noise LDO regulators providing 3.3V and 1.35V rails, with a voltage reference divider for DDR3.
- **Debugging and Indicators**: 6-pin JTAG header for firmware development and a power LED for status monitoring.
- **Board Specifications**: 60x40mm 4-layer PCB with EMI-optimized layout, via stitching, and assembly-friendly silkscreen.
- **Open-Source Assets**: Python scripts for schematic (SKiDL) and PCB (pcbnew) generation, KiCad files, Gerbers, BOM, and documentation.

## Key Components

### TMS320C6657 DSP (U1)
- **Manufacturer**: Texas Instruments
- **Type**: Dual-core C66x fixed and floating-point DSP
- **Clock Speed**: Up to 1.25 GHz per core
- **On-Chip Memory**: 32KB L1 program cache, 32KB L1 data cache, 1024KB L2 cache per core
- **Interfaces**: DDR3 EMIF (up to 8GB addressable, 1333 MT/s), USB 2.0 OTG, McASP for audio serial port, UART (2x), JTAG for debugging
- **Power**: Core supply 0.85–1.1V (nominal 1.0V), I/O 1.8V/3.3V
- **Package**: 625-pin BGA (21x21mm, 0.8mm pitch)
- **Operating Temperature**: -40°C to +100°C (commercial grade)
- **Key Notes**: Supports floating-point operations for precise audio processing; EMIF enables full utilization of 1GB DDR3 for buffering.

### MT41K512M16 RAM (U2)
- **Manufacturer**: Micron Technology
- **Type**: DDR3L SDRAM
- **Capacity**: 8Gb (512M x 16)
- **Speed**: 933 MHz (1866 MT/s)
- **Voltage**: 1.35V (VDD/VDDQ), compatible with 1.5V DDR3
- **Bus Width**: x16
- **Interfaces**: JEDEC-standard DDR3 with differential clock (CK/CK#), data strobes (LDQS/LDQS#, UDQS/UDQS#), masks (LDM/UDM), address (A0-15), bank (BA0-2), and control signals
- **Package**: 96-ball FBGA (9x14mm, 0.8mm pitch)
- **Operating Temperature**: -40°C to +95°C
- **Key Notes**: Provides 1GB for DSP buffering; requires initialization (mode registers, DLL) via firmware for reliable operation at high speeds.

### TAC5212 Audio Codec (U3)
- **Manufacturer**: Texas Instruments
- **Type**: Stereo audio codec with integrated ADC/DAC
- **Dynamic Range**: 119 dB ADC, 120 dB DAC (stereo mode)
- **Input/Output**: 2VRMS differential input/output, supporting single-ended via grounding negatives
- **Sample Rate**: Up to 192 kHz, 32-bit resolution
- **Interfaces**: I2S/TDM/LJ digital audio, with BCLK (bit clock), FSYNC (frame sync), DOUT (output), DIN (input)
- **Voltage**: Digital 1.0V (DREG), I/O 3.3V (IOVDD), analog 3.3V (AVDD)
- **Package**: VQFN-32 (5x5mm, 0.5mm pitch)
- **Operating Temperature**: -40°C to +125°C
- **Key Notes**: High SNR for professional audio; configure via registers for format/gain—use DSP McASP for direct interfacing.

### TPS7A54 LDO Regulators (U4 for 3.3V, U5 for 1.35V)
- **Manufacturer**: Texas Instruments
- **Type**: Low-noise, high-accuracy linear dropout regulator
- **Output Current**: Up to 4A
- **Accuracy**: 0.5% over temperature/line/load
- **Noise**: 4.4 µVRMS (10 Hz to 100 kHz)
- **Dropout Voltage**: 175 mV max at 4A
- **Input Voltage**: 1.1V to 6.5V
- **Package**: SOT-223-4 (with tab for heat sinking)
- **Operating Temperature**: -40°C to +125°C
- **Key Notes**: U4 steps down VBUS to 3.3V; U5 to 1.35V for DDR3 with feedback resistors (6.81k/10k for 1.35V output)—ideal for low-noise audio/DSP applications.

## Hardware Overview

The board is a 60x40mm 4-layer PCB (top signal, inner GND, inner power, bottom signal/AGND) optimized for high-speed signals and low noise.

- **Power Path**: USB VBUS (5V) through fuse (F1) to U4 (3.3V), which supplies U5 (1.35V for DDR3). VREF_DDR (0.675V) via divider (R3/R4, C_VREF). Star grounding minimizes noise coupling.
- **DSP-RAM Interface**: Complete DDR3 x16 bus with all signals connected; ZQ calibrated for impedance. Extensive decoupling near RAM.
- **Audio Path**: Stereo inputs/outputs with ESD; codec to DSP via McASP for synchronized digital audio.
- **USB**: OTG pins with protection; CC for detection.
- **Additional**: JTAG for debug, LED for power status.

## How It Works

1. **Power-Up**: USB connection supplies VBUS, regulated to stable rails. LED illuminates.
2. **USB Enumeration**: CC resistors enable device mode; DSP handles USB protocol for audio class.
3. **Audio Input**: Signals from J2 digitized by codec, sent to DSP via McASP.
4. **Processing**: DSP uses DDR3 for data, applies algorithms (e.g., effects).
5. **Audio Output**: Processed data back to codec for analog output on J3.
6. **Debug**: JTAG allows firmware loading/profiling.

Helpful tip: Ensure firmware initializes DDR3 timing parameters to match PCB trace lengths.

## What It Can Be Used For

- **Music Production**: Low-latency interface for recording/processing with onboard effects.
- **Live Audio**: Effects processor for instruments, leveraging RAM for delays.
- **IoT**: Edge audio analysis in smart devices.
- **Prototyping**: DSP development board with USB integration.
- **AI Audio**: Lightweight ML for voice tasks.

## Firmware Development Process

See detailed steps in the main README; uses TI tools like CCS and Processor SDK.

## Getting Started

1. **Generate Files**: Run schematic/PCB scripts to create KiCad files.
2. **KiCad Workflow**: Annotate, assign footprints, import netlist to PCB, run DRC/ERC.
3. **Fabrication**: Export Gerbers/BOM; use services like JLCPCB (specify impedance for DDR).
4. **Assembly**: Reflow for BGA; test power rails first.
5. **Firmware**: Load via JTAG using CCS.

Helpful tip: For DDR3, use TI EMIF tools in CCS for calibration.

## Contributing

Fork, modify, and PR. Comply with CERN-OHL-S v2; document changes.

## License

Copyright © 2025 DeMoD LLC and Asher LeRoy.

Licensed under CERN Open Hardware Licence Strongly Reciprocal (CERN-OHL-S) v2. See LICENSE for details.
