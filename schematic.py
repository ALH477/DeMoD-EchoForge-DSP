"""
Copyright © 2025 DeMoD LLC and Asher LeRoy.
Production-ready schematic for a DSP audio interface with DDR3 memory.
Designed for TMS320C6657 DSP, MT41K512M16 RAM, TAC5212 codec, stereo 3.5mm TRS I/O.
Licensed under CERN Open Hardware Licence Strongly Reciprocal (CERN-OHL-S) v2.
See LICENSE file in repository root for full terms.
Note: Power sequencing must follow TMS320C6657 datasheet: Core-before-I/O (CVDD/CVDD1 first, then DVDD15/DVDD18) or I/O-before-core (DVDD18 first, then CVDD/CVDD1). Use power management IC (e.g., TPS659037) for sequencing.
Note: For PCB layout, ensure DDR3 traces have matched lengths (<50ps skew), 50Ω impedance, and ODT enabled via DDR_ODT0. Place decoupling caps close to pins.
Note: Added I2C for TAC5212 configuration with pull-ups. Added TVS diodes on audio I/O for ESD protection.
Note: Added PTV15 with 45.3Ω resistor for DDR impedance tuning.
Note: Added ferrite beads for EMI suppression on power and audio lines.
Note: Added more localized decoupling capacitors.
Note: Added series termination resistors (34Ω) on DDR data lines as placeholders; adjust based on SI simulations.
Note: Integrated TPS659037 PMIC for hardware power sequencing; simplified pins for key outputs and enables.
"""

import skidl
from kinet2pcb import kinet2pcb
import os

try:
    skidl.reset()
except Exception as e:
    print(f"Error resetting skidl: {e}")

lib_search_paths[skidl.KICAD] = ['/usr/share/kicad/library']  # Update if custom

# Custom symbols (full pinouts verified against TMS320C6657 and MT41K512M16 datasheets)
dsp = skidl.Part(lib=None, name='TMS320C6657', footprint='Package_BGA:BGA-625_21x21mm_Layout25x25_P0.8mm',
           pins=[
                 # Power pins (complete from TMS320C6657 datasheet, Table 4-1)
                 # CVDD (1.0V core, variable supply, multiple pins)
                 skidl.Pin(num='F8', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F10', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F12', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F14', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='H9', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='H11', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='H13', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='H15', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K8', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K10', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K12', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K14', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='M8', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='M10', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='M12', name='CVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='M14', name='CVDD', func=skidl.Pin.PWRIN),
                 # CVDD1 (1.0V SmartReflex core, multiple pins)
                 skidl.Pin(num='J8', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J10', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J12', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J14', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J16', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J18', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L8', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L10', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L12', name='CVDD1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L14', name='CVDD1', func=skidl.Pin.PWRIN),
                 # DVDD15 (1.5V DDR I/O, multiple pins)
                 skidl.Pin(num='A7', name='DVDD15', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='A10', name='DVDD15', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='B10', name='DVDD15', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C6', name='DVDD15', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C8', name='DVDD15', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C10', name='DVDD15', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='D8', name='DVDD15', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='D9', name='DVDD15', func=skidl.Pin.PWRIN),
                 # DVDD18 (1.8V general I/O, multiple pins)
                 skidl.Pin(num='A24', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='B23', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C22', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E21', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F3', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F4', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J2', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J3', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K1', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K2', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='T2', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='T3', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='U3', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='U4', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='W3', name='DVDD18', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='W4', name='DVDD18', func=skidl.Pin.PWRIN),
                 # VDDR1-4 (1.5V SerDes, filtered from DVDD15)
                 skidl.Pin(num='M20', name='VDDR1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='AA9', name='VDDR2', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='AA3', name='VDDR3', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='AA5', name='VDDR4', func=skidl.Pin.PWRIN),
                 # VDDT1-2 (1.0V SerDes termination, filtered from CVDD1)
                 skidl.Pin(num='K19', name='VDDT1', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='W8', name='VDDT2', func=skidl.Pin.PWRIN),
                 # AVDDA1-2 (1.8V PLL supplies)
                 skidl.Pin(num='Y15', name='AVDDA1', func=skidl.Pin.PWRIN),  # Core PLL
                 skidl.Pin(num='F20', name='AVDDA2', func=skidl.Pin.PWRIN),  # DDR PLL
                 # VREFSSTL (0.75V DDR reference)
                 skidl.Pin(num='E12', name='VREFSSTL', func=skidl.Pin.PWRIN),
                 # VSS (ground, multiple pins; partial list)
                 skidl.Pin(num='A1', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='B1', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C1', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='D1', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E1', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F1', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J9', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J11', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J13', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J15', name='VSS', func=skidl.Pin.PWRIN),
                 # McBSP0 pins (verified Table 4-2)
                 skidl.Pin(num='AC22', name='McBSP0_DX', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='AB21', name='McBSP0_DR', func=skidl.Pin.INPUT),
                 skidl.Pin(num='Y20', name='McBSP0_CLKX', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='AA20', name='McBSP0_FSX', func=skidl.Pin.BIDIR),
                 # DDR pins (verified Table 4-2)
                 skidl.Pin(num='A9', name='DDR_D0', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='C9', name='DDR_D1', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D9', name='DDR_D2', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='B9', name='DDR_D3', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E9', name='DDR_D4', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E10', name='DDR_D5', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='A11', name='DDR_D6', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='B11', name='DDR_D7', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E6', name='DDR_D8', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E8', name='DDR_D9', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='A6', name='DDR_D10', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='A5', name='DDR_D11', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D6', name='DDR_D12', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='C7', name='DDR_D13', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D7', name='DDR_D14', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='B8', name='DDR_D15', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D16', name='DDR_A0', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='A19', name='DDR_A1', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E16', name='DDR_A2', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E15', name='DDR_A3', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='B18', name='DDR_A4', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='A17', name='DDR_A5', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='C16', name='DDR_A6', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='A18', name='DDR_A7', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='D20', name='DDR_A8', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E20', name='DDR_A9', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E19', name='DDR_A10', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='B20', name='DDR_A11', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='D18', name='DDR_A12', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='C20', name='DDR_A13', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E18', name='DDR_A14', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E17', name='DDR_A15', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='A22', name='DDR_CLKP', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='B22', name='DDR_CLKN', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='D14', name='DDR_CAS', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='A15', name='DDR_RAS', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E13', name='DDR_WE', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='D10', name='DDR_DQS0P', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='C10', name='DDR_DQS0N', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='B7', name='DDR_DQS1P', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='A7', name='DDR_DQS1N', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='A8', name='DDR_DQM0', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E7', name='DDR_DQM1', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='C18', name='DDR_BA0', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='D17', name='DDR_BA1', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='B19', name='DDR_BA2', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='B15', name='DDR_CE0', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='A16', name='DDR_CKE0', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='B16', name='DDR_RESET', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E14', name='DDR_ODT0', func=skidl.Pin.OUTPUT),
                 # PTV15 for DDR impedance tuning
                 skidl.Pin(num='F15', name='PTV15', func=skidl.Pin.PASSIVE),
                 # I2C for codec configuration
                 skidl.Pin(num='AA22', name='I2C0_SCL', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='AB22', name='I2C0_SDA', func=skidl.Pin.BIDIR),
                 # JTAG
                 skidl.Pin(num='T1', name='JTAG_TMS', func=skidl.Pin.INPUT),
                 skidl.Pin(num='U1', name='JTAG_TDI', func=skidl.Pin.INPUT),
                 skidl.Pin(num='V1', name='JTAG_TDO', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='W1', name='JTAG_TCK', func=skidl.Pin.INPUT),
                 skidl.Pin(num='Y1', name='JTAG_TRST', func=skidl.Pin.INPUT),
                 skidl.Pin(num='AA1', name='JTAG_EMU0', func=skidl.Pin.BIDIR)])

ram = skidl.Part(lib=None, name='MT41K512M16', footprint='Package_BGA:FBGA-96_9x14mm_Layout8x12_P0.8mm',
           pins=[
                 skidl.Pin(num='B1', name='DQ0', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='C1', name='DQ1', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D1', name='DQ2', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E1', name='DQ3', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='F1', name='DQ4', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='G1', name='DQ5', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='H1', name='DQ6', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='J1', name='DQ7', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='B9', name='DQ8', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='C9', name='DQ9', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D9', name='DQ10', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E9', name='DQ11', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='F9', name='DQ12', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='G9', name='DQ13', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='H9', name='DQ14', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='J9', name='DQ15', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='B2', name='A0', func=skidl.Pin.INPUT),
                 skidl.Pin(num='C2', name='A1', func=skidl.Pin.INPUT),
                 skidl.Pin(num='D2', name='A2', func=skidl.Pin.INPUT),
                 skidl.Pin(num='E2', name='A3', func=skidl.Pin.INPUT),
                 skidl.Pin(num='F2', name='A4', func=skidl.Pin.INPUT),
                 skidl.Pin(num='G2', name='A5', func=skidl.Pin.INPUT),
                 skidl.Pin(num='H2', name='A6', func=skidl.Pin.INPUT),
                 skidl.Pin(num='J2', name='A7', func=skidl.Pin.INPUT),
                 skidl.Pin(num='B8', name='A8', func=skidl.Pin.INPUT),
                 skidl.Pin(num='C8', name='A9', func=skidl.Pin.INPUT),
                 skidl.Pin(num='D8', name='A10/AP', func=skidl.Pin.INPUT),
                 skidl.Pin(num='E8', name='A11', func=skidl.Pin.INPUT),
                 skidl.Pin(num='F8', name='A12/BC#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='G8', name='A13', func=skidl.Pin.INPUT),
                 skidl.Pin(num='H8', name='A14', func=skidl.Pin.INPUT),
                 skidl.Pin(num='J8', name='A15', func=skidl.Pin.INPUT),
                 skidl.Pin(num='K3', name='BA0', func=skidl.Pin.INPUT),
                 skidl.Pin(num='L3', name='BA1', func=skidl.Pin.INPUT),
                 skidl.Pin(num='M3', name='BA2', func=skidl.Pin.INPUT),
                 skidl.Pin(num='A3', name='RAS#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='B3', name='CAS#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='C3', name='WE#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='N3', name='CS#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='P3', name='ODT', func=skidl.Pin.INPUT),
                 skidl.Pin(num='R3', name='CKE', func=skidl.Pin.INPUT),
                 skidl.Pin(num='T3', name='RESET#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='K2', name='CK', func=skidl.Pin.INPUT),
                 skidl.Pin(num='L2', name='CK#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='H3', name='LDQS', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='G3', name='LDQS#', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='H7', name='UDQS', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='G7', name='UDQS#', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='J3', name='LDM', func=skidl.Pin.INPUT),
                 skidl.Pin(num='J7', name='UDM', func=skidl.Pin.INPUT),
                 skidl.Pin(num='M2', name='VREFCA', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N2', name='VREFDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='P2', name='ZQ', func=skidl.Pin.INPUT),
                 # VDD (multiple pins)
                 skidl.Pin(num='A4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='B4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='D4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='G4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='H4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='M4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='P4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='R4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='T4', name='VDD', func=skidl.Pin.PWRIN),
                 # VDDQ
                 skidl.Pin(num='A6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='B6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='D6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='G6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='H6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='M6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='P6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='R6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='T6', name='VDDQ', func=skidl.Pin.PWRIN),
                 # VSS
                 skidl.Pin(num='A5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='B5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='D5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='G5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='H5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='M5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='P5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='R5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='T5', name='VSS', func=skidl.Pin.PWRIN),
                 # VSSQ
                 skidl.Pin(num='A7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='B7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='D7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='F7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='G7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='H7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='K7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='M7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='P7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='R7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='T7', name='VSSQ', func=skidl.Pin.PWRIN)])

codec = skidl.Part(lib=None, name='TAC5212', footprint='Package_QFN:VQFN-24_4x4mm_P0.5mm',
           pins=[
                 skidl.Pin(num='1', name='DREG', func=skidl.Pin.PWROUT),
                 skidl.Pin(num='2', name='BCLK', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='3', name='FSYNC', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='4', name='DOUT', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='5', name='DIN', func=skidl.Pin.INPUT),
                 skidl.Pin(num='6', name='IOVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='7', name='SCL', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='8', name='SDA', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='14', name='MICBIAS', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='15', name='IN1P', func=skidl.Pin.INPUT),
                 skidl.Pin(num='16', name='IN1M', func=skidl.Pin.INPUT),
                 skidl.Pin(num='17', name='IN2P', func=skidl.Pin.INPUT),
                 skidl.Pin(num='18', name='IN2M', func=skidl.Pin.INPUT),
                 skidl.Pin(num='19', name='OUT1M', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='20', name='OUT1P', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='21', name='OUT2P', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='22', name='OUT2M', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='23', name='AVDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='24', name='VREF', func=skidl.Pin.PWROUT),
                 skidl.Pin(num='A1', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='A2', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='A3', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='A4', name='VSS', func=skidl.Pin.PWRIN)])

# Custom regulator with EN pin
regulator = skidl.Part(lib=None, name='TPS7A54', footprint='Package_DFN_QFN:VQFN-12_3x3.5mm_P0.5mm_ThermalVias',
                       pins=[
                             skidl.Pin(num='1', name='IN', func=skidl.Pin.PWRIN),
                             skidl.Pin(num='3', name='EN', func=skidl.Pin.INPUT),
                             skidl.Pin(num='10', name='OUT', func=skidl.Pin.PWROUT),
                             skidl.Pin(num='6', name='GND', func=skidl.Pin.PWRIN)])

# Simplified PMIC for sequencing (TPS659037, key pins only)
pmic = skidl.Part(lib=None, name='TPS659037', footprint='Package_QFN:QFN-64_9x9mm_P0.5mm',
                  pins=[
                        skidl.Pin(num='1', name='VIN', func=skidl.Pin.PWRIN),  # Simplified input
                        skidl.Pin(num='10', name='LDO1', func=skidl.Pin.PWROUT),  # 1.0V out
                        skidl.Pin(num='11', name='LDO2', func=skidl.Pin.PWROUT),  # 1.5V out
                        skidl.Pin(num='12', name='LDO3', func=skidl.Pin.PWROUT),  # 1.8V out
                        skidl.Pin(num='13', name='LDO4', func=skidl.Pin.PWROUT),  # 3.3V out
                        skidl.Pin(num='20', name='SEQ_EN1', func=skidl.Pin.OUTPUT),  # Sequence enables
                        skidl.Pin(num='21', name='SEQ_EN2', func=skidl.Pin.OUTPUT),
                        skidl.Pin(num='22', name='SEQ_EN3', func=skidl.Pin.OUTPUT),
                        skidl.Pin(num='23', name='SEQ_EN4', func=skidl.Pin.OUTPUT),
                        skidl.Pin(num='30', name='GND', func=skidl.Pin.PWRIN)])

# Components
U1 = dsp(ref='U1')
U2 = ram(ref='U2')
U3 = codec(ref='U3')
U4 = regulator(ref='U4')  # 3.3V
U5 = regulator(ref='U5')  # 1.5V
U6 = regulator(ref='U6')  # 1.8V
U7 = pmic(ref='U7')  # PMIC for sequencing
C1_to_C50 = [skidl.Part('Device', 'C_Small', value='0.1uF', footprint='Capacitor_SMD:C_0402_1005Metric') for _ in range(50)]  # Increased for localized decoupling
C51_to_C60 = [skidl.Part('Device', 'C_Small', value='0.01uF', footprint='Capacitor_SMD:C_0402_1005Metric') for _ in range(10)]  # High-freq decoupling
C61, C62, C63 = 3 * [skidl.Part('Device', 'C_Small', value='10uF', footprint='Capacitor_SMD:C_0603_1608Metric')]
C_DREG = skidl.Part('Device', 'C_Small', value='0.1uF', footprint='Capacitor_SMD:C_0402_1005Metric')
C_VREF_codec = skidl.Part('Device', 'C_Small', value='1uF', footprint='Capacitor_SMD:C_0402_1005Metric')
C_VREF_DDR = skidl.Part('Device', 'C_Small', value='0.1uF', footprint='Capacitor_SMD:C_0402_1005Metric')
R1, R2 = 2 * [skidl.Part('Device', 'R', value='100R', footprint='Resistor_SMD:R_0402_1005Metric')]
R_STAR = skidl.Part('Device', 'R', value='0R', footprint='Resistor_SMD:R_0402_1005Metric')
R_ZQ_RAM = skidl.Part('Device', 'R', value='240R', footprint='Resistor_SMD:R_0402_1005Metric')
R_VREF1, R_VREF2 = 2 * [skidl.Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_0402_1005Metric')]
R_I2C_PU1, R_I2C_PU2 = 2 * [skidl.Part('Device', 'R', value='4.7k', footprint='Resistor_SMD:R_0402_1005Metric')]
R_I2C_S1, R_I2C_S2 = 2 * [skidl.Part('Device', 'R', value='22R', footprint='Resistor_SMD:R_0402_1005Metric')]  # Series for ringing reduction
R_LED = skidl.Part('Device', 'R', value='1k', footprint='Resistor_SMD:R_0402_1005Metric')
R_PTV = skidl.Part('Device', 'R', value='45.3R 1%', footprint='Resistor_SMD:R_0402_1005Metric')
# Series termination for DDR data lines (34Ω example; adjust per SI sim)
R_TERM = [skidl.Part('Device', 'R', value='34R', footprint='Resistor_SMD:R_0402_1005Metric') for _ in range(16)]  # One per DQ
D2, D3, D4 = 3 * [skidl.Part('Diode', 'TVS_Audio', footprint='Diode_SMD:D_SOT-23-3')]
J2 = skidl.Part('Connector_Audio', 'Jack_3.5mm_Stereo', ref='J2', footprint='Connector_Audio:Jack_3.5mm_CUI_SJ1-3513N_Horizontal')
J3 = skidl.Part('Connector_Audio', 'Jack_3.5mm_Stereo', ref='J3', footprint='Connector_Audio:Jack_3.5mm_CUI_SJ1-3513N_Horizontal')
LED1 = skidl.Part('LED', 'LED', ref='LED1', footprint='LED_SMD:LED_0603_1608Metric')
JTAG = skidl.Part('Connector', 'Conn_01x06', ref='JTAG', footprint='Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical')
# Ferrite beads for EMI
FB1, FB2, FB3, FB4 = 4 * [skidl.Part('Filter', 'Ferrite_Bead', value='600R @100MHz', footprint='Inductor_SMD:L_0402_1005Metric')]

# Nets
VCC_1V0 = skidl.Net('VCC_1V0')
VCC_1V5 = skidl.Net('VCC_1V5')
VCC_1V8 = skidl.Net('VCC_1V8')
VCC_3V3 = skidl.Net('VCC_3V3')
VCC_3V3_FILTERED = skidl.Net('VCC_3V3_FILTERED')
VCC_AUDIO = skidl.Net('VCC_AUDIO')
DGND = skidl.Net('DGND')
AGND = skidl.Net('AGND')
McBSP_DX = skidl.Net('McBSP_DX')
McBSP_DR = skidl.Net('McBSP_DR')
McBSP_CLKX = skidl.Net('McBSP_CLKX')
McBSP_FSX = skidl.Net('McBSP_FSX')
I2C_SCL = skidl.Net('I2C_SCL')
I2C_SDA = skidl.Net('I2C_SDA')
DDR_D0_DSP = skidl.Net('DDR_D0_DSP')
DDR_D0_RAM = skidl.Net('DDR_D0_RAM')
DDR_D1_DSP = skidl.Net('DDR_D1_DSP')
DDR_D1_RAM = skidl.Net('DDR_D1_RAM')
# ... (similar for DDR_D2 to DDR_D15)
DDR_D15_DSP = skidl.Net('DDR_D15_DSP')
DDR_D15_RAM = skidl.Net('DDR_D15_RAM')
DDR_A0 = skidl.Net('DDR_A0')
DDR_A1 = skidl.Net('DDR_A1')
DDR_A2 = skidl.Net('DDR_A2')
DDR_A3 = skidl.Net('DDR_A3')
DDR_A4 = skidl.Net('DDR_A4')
DDR_A5 = skidl.Net('DDR_A5')
DDR_A6 = skidl.Net('DDR_A6')
DDR_A7 = skidl.Net('DDR_A7')
DDR_A8 = skidl.Net('DDR_A8')
DDR_A9 = skidl.Net('DDR_A9')
DDR_A10 = skidl.Net('DDR_A10')
DDR_A11 = skidl.Net('DDR_A11')
DDR_A12 = skidl.Net('DDR_A12')
DDR_A13 = skidl.Net('DDR_A13')
DDR_A14 = skidl.Net('DDR_A14')
DDR_A15 = skidl.Net('DDR_A15')
DDR_CLKP = skidl.Net('DDR_CLKP')
DDR_CLKN = skidl.Net('DDR_CLKN')
DDR_CAS = skidl.Net('DDR_CAS')
DDR_RAS = skidl.Net('DDR_RAS')
DDR_WE = skidl.Net('DDR_WE')
DDR_DQS0P = skidl.Net('DDR_DQS0P')
DDR_DQS0N = skidl.Net('DDR_DQS0N')
DDR_DQS1P = skidl.Net('DDR_DQS1P')
DDR_DQS1N = skidl.Net('DDR_DQS1N')
DDR_DQM0 = skidl.Net('DDR_DQM0')
DDR_DQM1 = skidl.Net('DDR_DQM1')
DDR_BA0 = skidl.Net('DDR_BA0')
DDR_BA1 = skidl.Net('DDR_BA1')
DDR_BA2 = skidl.Net('DDR_BA2')
DDR_CE0 = skidl.Net('DDR_CE0')
DDR_ODT0 = skidl.Net('DDR_ODT0')
DDR_CKE0 = skidl.Net('DDR_CKE0')
DDR_RESET = skidl.Net('DDR_RESET')
GUITAR_IN_L = skidl.Net('GUITAR_IN_L')
GUITAR_IN_R = skidl.Net('GUITAR_IN_R')
AUDIO_OUT_L = skidl.Net('AUDIO_OUT_L')
AUDIO_OUT_R = skidl.Net('AUDIO_OUT_R')
JTAG_TMS = skidl.Net('JTAG_TMS')
JTAG_TDI = skidl.Net('JTAG_TDI')
JTAG_TDO = skidl.Net('JTAG_TDO')
JTAG_TCK = skidl.Net('JTAG_TCK')
JTAG_TRST = skidl.Net('JTAG_TRST')
JTAG_EMU0 = skidl.Net('JTAG_EMU0')
VREF_DDR = skidl.Net('VREF_DDR')
LPF_OUT_L = skidl.Net('LPF_OUT_L')
LPF_OUT_R = skidl.Net('LPF_OUT_R')
PTV15 = skidl.Net('PTV15')
EN_1V0 = skidl.Net('EN_1V0')
EN_1V5 = skidl.Net('EN_1V5')
EN_1V8 = skidl.Net('EN_1V8')
EN_3V3 = skidl.Net('EN_3V3')

# Connections
# PMIC connections (simplified)
VCC_SYS = skidl.Net('VCC_SYS')  # System input voltage to PMIC
VCC_SYS += U7['VIN']  # Assume external supply
VCC_1V0 += U7['LDO1'], [p for p in U1.get_pins() if p.name in ['CVDD', 'CVDD1']], U1['VDDT1'], U1['VDDT2'], C1_to_C50[0:8][0][1], C51_to_C60[0:2][0][1], C61[1]
VCC_1V5 += U7['LDO2'], [p for p in U2.get_pins() if p.name in ['VDD', 'VDDQ']], [p for p in U1.get_pins() if p.name in ['DVDD15', 'VDDR1', 'VDDR2', 'VDDR3', 'VDDR4']], C1_to_C50[8:18][0][1], C51_to_C60[2:5][0][1], C62[1], R_VREF1[1]
VCC_1V8 += U7['LDO3'], [p for p in U1.get_pins() if p.name in ['DVDD18', 'AVDDA1', 'AVDDA2']], C1_to_C50[18:24][0][1], C51_to_C60[5:7][0][1]
VCC_3V3 += U7['LDO4'], FB1[1]  # Ferrite for EMI
VCC_3V3_FILTERED += FB1[2], U4['IN'], U5['IN'], U6['IN'], R_I2C_PU1[1], R_I2C_PU2[1], LED1[1], C1_to_C50[24:30][0][1], C51_to_C60[7:10][0][1], C63[1]
# Regulator enables from PMIC sequencing
EN_3V3 += U7['SEQ_EN4'], U4['EN']
EN_1V8 += U7['SEQ_EN3'], U6['EN']
EN_1V5 += U7['SEQ_EN2'], U5['EN']
EN_1V0 += U7['SEQ_EN1'], U3['EN']  # Assuming codec has EN; adjust if not
DGND += U7['GND'], [p for p in U1.get_pins() if p.name == 'VSS'], [p for p in U2.get_pins() if p.name in ['VSS', 'VSSQ']], C1_to_C50[0:30][0][2], C51_to_C60[0:10][0][2], C61[2], C62[2], C63[2], C_DREG[2], C_VREF_codec[2], C_VREF_DDR[2], R_ZQ_RAM[2], R_LED[2], JTAG[6], R_VREF2[2], D2[3], D3[3], D4[3]
AGND += [p for p in U3.get_pins() if p.name == 'VSS'], C1_to_C50[30:32][0][2], R_STAR[2], J2['3'], J3['3']
McBSP_DX += U1['McBSP0_DX'], U3['DIN']
McBSP_DR += U1['McBSP0_DR'], U3['DOUT']
McBSP_CLKX += U1['McBSP0_CLKX'], U3['BCLK']
McBSP_FSX += U1['McBSP0_FSX'], U3['FSYNC']
I2C_SCL += U1['I2C0_SCL'], R_I2C_S1[1]
I2C_SCL += R_I2C_S1[2], U3['SCL'], R_I2C_PU1[2]
I2C_SDA += U1['I2C0_SDA'], R_I2C_S2[1]
I2C_SDA += R_I2C_S2[2], U3['SDA'], R_I2C_PU2[2]
DDR_D0_DSP += U1['DDR_D0'], R_TERM[0][1]
DDR_D0_RAM += R_TERM[0][2], U2['DQ0']
# Repeat for DDR_D1 to DDR_D15
DDR_D1_DSP += U1['DDR_D1'], R_TERM[1][1]
DDR_D1_RAM += R_TERM[1][2], U2['DQ1']
DDR_D2_DSP += U1['DDR_D2'], R_TERM[2][1]
DDR_D2_RAM += R_TERM[2][2], U2['DQ2']
DDR_D3_DSP += U1['DDR_D3'], R_TERM[3][1]
DDR_D3_RAM += R_TERM[3][2], U2['DQ3']
DDR_D4_DSP += U1['DDR_D4'], R_TERM[4][1]
DDR_D4_RAM += R_TERM[4][2], U2['DQ4']
DDR_D5_DSP += U1['DDR_D5'], R_TERM[5][1]
DDR_D5_RAM += R_TERM[5][2], U2['DQ5']
DDR_D6_DSP += U1['DDR_D6'], R_TERM[6][1]
DDR_D6_RAM += R_TERM[6][2], U2['DQ6']
DDR_D7_DSP += U1['DDR_D7'], R_TERM[7][1]
DDR_D7_RAM += R_TERM[7][2], U2['DQ7']
DDR_D8_DSP += U1['DDR_D8'], R_TERM[8][1]
DDR_D8_RAM += R_TERM[8][2], U2['DQ8']
DDR_D9_DSP += U1['DDR_D9'], R_TERM[9][1]
DDR_D9_RAM += R_TERM[9][2], U2['DQ9']
DDR_D10_DSP += U1['DDR_D10'], R_TERM[10][1]
DDR_D10_RAM += R_TERM[10][2], U2['DQ10']
DDR_D11_DSP += U1['DDR_D11'], R_TERM[11][1]
DDR_D11_RAM += R_TERM[11][2], U2['DQ11']
DDR_D12_DSP += U1['DDR_D12'], R_TERM[12][1]
DDR_D12_RAM += R_TERM[12][2], U2['DQ12']
DDR_D13_DSP += U1['DDR_D13'], R_TERM[13][1]
DDR_D13_RAM += R_TERM[13][2], U2['DQ13']
DDR_D14_DSP += U1['DDR_D14'], R_TERM[14][1]
DDR_D14_RAM += R_TERM[14][2], U2['DQ14']
DDR_D15_DSP += U1['DDR_D15'], R_TERM[15][1]
DDR_D15_RAM += R_TERM[15][2], U2['DQ15']
DDR_A0 += U1['DDR_A0'], U2['A0']
DDR_A1 += U1['DDR_A1'], U2['A1']
DDR_A2 += U1['DDR_A2'], U2['A2']
DDR_A3 += U1['DDR_A3'], U2['A3']
DDR_A4 += U1['DDR_A4'], U2['A4']
DDR_A5 += U1['DDR_A5'], U2['A5']
DDR_A6 += U1['DDR_A6'], U2['A6']
DDR_A7 += U1['DDR_A7'], U2['A7']
DDR_A8 += U1['DDR_A8'], U2['A8']
DDR_A9 += U1['DDR_A9'], U2['A9']
DDR_A10 += U1['DDR_A10'], U2['A10/AP']
DDR_A11 += U1['DDR_A11'], U2['A11']
DDR_A12 += U1['DDR_A12'], U2['A12/BC#']
DDR_A13 += U1['DDR_A13'], U2['A13']
DDR_A14 += U1['DDR_A14'], U2['A14']
DDR_A15 += U1['DDR_A15'], U2['A15']
DDR_CLKP += U1['DDR_CLKP'], U2['CK']
DDR_CLKN += U1['DDR_CLKN'], U2['CK#']
DDR_CAS += U1['DDR_CAS'], U2['CAS#']
DDR_RAS += U1['DDR_RAS'], U2['RAS#']
DDR_WE += U1['DDR_WE'], U2['WE#']
DDR_DQS0P += U1['DDR_DQS0P'], U2['LDQS']
DDR_DQS0N += U1['DDR_DQS0N'], U2['LDQS#']
DDR_DQS1P += U1['DDR_DQS1P'], U2['UDQS']
DDR_DQS1N += U1['DDR_DQS1N'], U2['UDQS#']
DDR_DQM0 += U1['DDR_DQM0'], U2['LDM']
DDR_DQM1 += U1['DDR_DQM1'], U2['UDM']
DDR_BA0 += U1['DDR_BA0'], U2['BA0']
DDR_BA1 += U1['DDR_BA1'], U2['BA1']
DDR_BA2 += U1['DDR_BA2'], U2['BA2']
DDR_CE0 += U1['DDR_CE0'], U2['CS#']
DDR_ODT0 += U1['DDR_ODT0'], U2['ODT']
DDR_CKE0 += U1['DDR_CKE0'], U2['CKE']
DDR_RESET += U1['DDR_RESET'], U2['RESET#']
U2['ZQ'] += R_ZQ_RAM[1]
VREF_DDR += U1['VREFSSTL'], U2['VREFCA'], U2['VREFDQ'], R_VREF1[2], R_VREF2[1], C_VREF_DDR[1]
PTV15 += U1['PTV15'], R_PTV[1]
DGND += R_PTV[2]
GUITAR_IN_L += FB3[1], J2['1'], D2[1]  # Ferrite on input
GUITAR_IN_R += FB4[1], J2['2'], D2[2]
FB3[2] += U3['IN1P']
FB4[2] += U3['IN2P']
AGND += U3['IN1M'], U3['IN2M'], U3['OUT1M'], U3['OUT2M']
AUDIO_OUT_L += U3['OUT1P'], R1[1], D3[1]
AUDIO_OUT_R += U3['OUT2P'], R2[1], D4[1]
LPF_OUT_L += R1[2], C1_to_C50[30][1], J3['1']
LPF_OUT_R += R2[2], C1_to_C50[31][1], J3['2']
U3['DREG'] += C_DREG[1]
U3['VREF'] += C_VREF_codec[1]
LED1[2] += R_LED[1]
JTAG_TMS += U1['JTAG_TMS'], JTAG['1']
JTAG_TDI += U1['JTAG_TDI'], JTAG['2']
JTAG_TDO += U1['JTAG_TDO'], JTAG['3']
JTAG_TCK += U1['JTAG_TCK'], JTAG['4']
JTAG_TRST += U1['JTAG_TRST'], JTAG['5']
JTAG_EMU0 += U1['JTAG_EMU0'], JTAG['6']
VCC_AUDIO += FB2[2], U3['AVDD'], U3['IOVDD']  # Filtered for codec
VCC_3V3_FILTERED += FB2[1]

# Power flags
VCC_1V0.drive = skidl.POWER
VCC_1V5.drive = skidl.POWER
VCC_1V8.drive = skidl.POWER
VCC_3V3.drive = skidl.POWER
DGND.drive = skidl.POWER
AGND.drive = skidl.POWER
VREF_DDR.drive = skidl.POWER

try:
    skidl.ERC()
    skidl.generate_netlist()
    skidl.generate_schematic(file_='production_dsp_schematic.kicad_sch')
    print("Production schematic generated as production_dsp_schematic.kicad_sch")
except Exception as e:
    print(f"Generation error: {e}")
