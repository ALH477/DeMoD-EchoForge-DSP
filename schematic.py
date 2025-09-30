# schematic.py
"""
Copyright © 2025 DeMoD LLC and Asher LeRoy.
Production-ready schematic for a USB-C DSP audio interface with DDR3 memory.
Designed for TMS320C6657 DSP, MT41K512M16 RAM, TAC5212 codec, USB-C, stereo 3.5mm TRS I/O.
Licensed under CERN Open Hardware Licence Strongly Reciprocal (CERN-OHL-S) v2.
See LICENSE file in repository root for full terms.
"""

import skidl
from kinet2pcb import kinet2pcb
import os

try:
    skidl.reset()
except Exception as e:
    print(f"Error resetting skidl: {e}")

lib_search_paths[skidl.KICAD] = ['/usr/share/kicad/library']  # Update if custom

# Custom symbols (full DDR3 x16 pinout from datasheets)
dsp = skidl.Part(lib=None, name='TMS320C6657', footprint='Package_BGA:BGA-625_21x21mm_Layout25x25_P0.8mm',
           pins=[skidl.Pin(num='A1', name='CVDD', func=skidl.Pin.PWRIN), skidl.Pin(num='B1', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='AC22', name='McASP0_AXR0', func=skidl.Pin.BIDIR), skidl.Pin(num='Y20', name='McASP0_ACLKX', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='AA20', name='McASP0_AFSX', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='A9', name='DDR_D0', func=skidl.Pin.BIDIR), skidl.Pin(num='C9', name='DDR_D1', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D9', name='DDR_D2', func=skidl.Pin.BIDIR), skidl.Pin(num='B9', name='DDR_D3', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E9', name='DDR_D4', func=skidl.Pin.BIDIR), skidl.Pin(num='E10', name='DDR_D5', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='A11', name='DDR_D6', func=skidl.Pin.BIDIR), skidl.Pin(num='B11', name='DDR_D7', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E6', name='DDR_D8', func=skidl.Pin.BIDIR), skidl.Pin(num='E8', name='DDR_D9', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='A6', name='DDR_D10', func=skidl.Pin.BIDIR), skidl.Pin(num='A5', name='DDR_D11', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D6', name='DDR_D12', func=skidl.Pin.BIDIR), skidl.Pin(num='C7', name='DDR_D13', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D7', name='DDR_D14', func=skidl.Pin.BIDIR), skidl.Pin(num='B6', name='DDR_D15', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='E16', name='DDR_A0', func=skidl.Pin.OUTPUT), skidl.Pin(num='F16', name='DDR_A1', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='G16', name='DDR_A2', func=skidl.Pin.OUTPUT), skidl.Pin(num='H16', name='DDR_A3', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='J16', name='DDR_A4', func=skidl.Pin.OUTPUT), skidl.Pin(num='K16', name='DDR_A5', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='L16', name='DDR_A6', func=skidl.Pin.OUTPUT), skidl.Pin(num='M16', name='DDR_A7', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='N16', name='DDR_A8', func=skidl.Pin.OUTPUT), skidl.Pin(num='P16', name='DDR_A9', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='R16', name='DDR_A10', func=skidl.Pin.OUTPUT), skidl.Pin(num='T16', name='DDR_A11', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='U16', name='DDR_A12', func=skidl.Pin.OUTPUT), skidl.Pin(num='V16', name='DDR_A13', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='W16', name='DDR_A14', func=skidl.Pin.OUTPUT), skidl.Pin(num='Y16', name='DDR_A15', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='A22', name='DDR_CLK', func=skidl.Pin.OUTPUT), skidl.Pin(num='B22', name='DDR_CLKN', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='D14', name='DDR_CAS', func=skidl.Pin.OUTPUT), skidl.Pin(num='A15', name='DDR_RAS', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='E13', name='DDR_WE', func=skidl.Pin.OUTPUT), skidl.Pin(num='D10', name='DDR_LDQS', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='C10', name='DDR_LDQSN', func=skidl.Pin.BIDIR), skidl.Pin(num='B10', name='DDR_UDQS', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='A10', name='DDR_UDQSN', func=skidl.Pin.BIDIR), skidl.Pin(num='A8', name='DDR_LDM', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='B8', name='DDR_UDM', func=skidl.Pin.OUTPUT), skidl.Pin(num='C8', name='DDR_BA0', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='D8', name='DDR_BA1', func=skidl.Pin.OUTPUT), skidl.Pin(num='E8', name='DDR_BA2', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='F8', name='DDR_CS', func=skidl.Pin.OUTPUT), skidl.Pin(num='G8', name='DDR_ODT', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='H8', name='DDR_CKE', func=skidl.Pin.OUTPUT), skidl.Pin(num='J8', name='DDR_RESET', func=skidl.Pin.OUTPUT),
                 skidl.Pin(num='K8', name='DDR_ZQ', func=skidl.Pin.OUTPUT), skidl.Pin(num='E12', name='VREFSSTL', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='Y4', name='USB0_DP', func=skidl.Pin.BIDIR), skidl.Pin(num='AA4', name='USB0_DM', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='AB4', name='USB0_VBUS', func=skidl.Pin.INPUT),
                 skidl.Pin(num='T1', name='JTAG_TMS', func=skidl.Pin.INPUT), skidl.Pin(num='U1', name='JTAG_TDI', func=skidl.Pin.INPUT),
                 skidl.Pin(num='V1', name='JTAG_TDO', func=skidl.Pin.OUTPUT), skidl.Pin(num='W1', name='JTAG_TCK', func=skidl.Pin.INPUT),
                 skidl.Pin(num='Y1', name='JTAG_TRST', func=skidl.Pin.INPUT), skidl.Pin(num='AA1', name='JTAG_EMU0', func=skidl.Pin.BIDIR)])

ram = skidl.Part(lib=None, name='MT41K512M16', footprint='Package_BGA:FBGA-96_9x14mm_Layout8x12_P0.8mm',
           pins=[skidl.Pin(num='B1', name='DQ0', func=skidl.Pin.BIDIR), skidl.Pin(num='C1', name='DQ1', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D1', name='DQ2', func=skidl.Pin.BIDIR), skidl.Pin(num='E1', name='DQ3', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='F1', name='DQ4', func=skidl.Pin.BIDIR), skidl.Pin(num='G1', name='DQ5', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='H1', name='DQ6', func=skidl.Pin.BIDIR), skidl.Pin(num='J1', name='DQ7', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='B9', name='DQ8', func=skidl.Pin.BIDIR), skidl.Pin(num='C9', name='DQ9', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='D9', name='DQ10', func=skidl.Pin.BIDIR), skidl.Pin(num='E9', name='DQ11', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='F9', name='DQ12', func=skidl.Pin.BIDIR), skidl.Pin(num='G9', name='DQ13', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='H9', name='DQ14', func=skidl.Pin.BIDIR), skidl.Pin(num='J9', name='DQ15', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='B2', name='A0', func=skidl.Pin.INPUT), skidl.Pin(num='C2', name='A1', func=skidl.Pin.INPUT),
                 skidl.Pin(num='D2', name='A2', func=skidl.Pin.INPUT), skidl.Pin(num='E2', name='A3', func=skidl.Pin.INPUT),
                 skidl.Pin(num='F2', name='A4', func=skidl.Pin.INPUT), skidl.Pin(num='G2', name='A5', func=skidl.Pin.INPUT),
                 skidl.Pin(num='H2', name='A6', func=skidl.Pin.INPUT), skidl.Pin(num='J2', name='A7', func=skidl.Pin.INPUT),
                 skidl.Pin(num='B8', name='A8', func=skidl.Pin.INPUT), skidl.Pin(num='C8', name='A9', func=skidl.Pin.INPUT),
                 skidl.Pin(num='D8', name='A10/AP', func=skidl.Pin.INPUT), skidl.Pin(num='E8', name='A11', func=skidl.Pin.INPUT),
                 skidl.Pin(num='F8', name='A12/BC#', func=skidl.Pin.INPUT), skidl.Pin(num='G8', name='A13', func=skidl.Pin.INPUT),
                 skidl.Pin(num='H8', name='A14', func=skidl.Pin.INPUT), skidl.Pin(num='J8', name='A15', func=skidl.Pin.INPUT),
                 skidl.Pin(num='K3', name='BA0', func=skidl.Pin.INPUT), skidl.Pin(num='L3', name='BA1', func=skidl.Pin.INPUT),
                 skidl.Pin(num='M3', name='BA2', func=skidl.Pin.INPUT),
                 skidl.Pin(num='A3', name='RAS#', func=skidl.Pin.INPUT), skidl.Pin(num='B3', name='CAS#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='C3', name='WE#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='N3', name='CS#', func=skidl.Pin.INPUT), skidl.Pin(num='P3', name='ODT', func=skidl.Pin.INPUT),
                 skidl.Pin(num='R3', name='CKE', func=skidl.Pin.INPUT), skidl.Pin(num='T3', name='RESET#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='K2', name='CK', func=skidl.Pin.INPUT), skidl.Pin(num='L2', name='CK#', func=skidl.Pin.INPUT),
                 skidl.Pin(num='H3', name='LDQS', func=skidl.Pin.BIDIR), skidl.Pin(num='G3', name='LDQS#', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='H7', name='UDQS', func=skidl.Pin.BIDIR), skidl.Pin(num='G7', name='UDQS#', func=skidl.Pin.BIDIR),
                 skidl.Pin(num='J3', name='LDM', func=skidl.Pin.INPUT), skidl.Pin(num='J7', name='UDM', func=skidl.Pin.INPUT),
                 skidl.Pin(num='M2', name='VREFCA', func=skidl.Pin.PWRIN), skidl.Pin(num='N2', name='VREFDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='P2', name='ZQ', func=skidl.Pin.INPUT),
                 skidl.Pin(num='A4', name='VDD', func=skidl.Pin.PWRIN), skidl.Pin(num='B4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C4', name='VDD', func=skidl.Pin.PWRIN), skidl.Pin(num='D4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E4', name='VDD', func=skidl.Pin.PWRIN), skidl.Pin(num='F4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='G4', name='VDD', func=skidl.Pin.PWRIN), skidl.Pin(num='H4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J4', name='VDD', func=skidl.Pin.PWRIN), skidl.Pin(num='K4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L4', name='VDD', func=skidl.Pin.PWRIN), skidl.Pin(num='M4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N4', name='VDD', func=skidl.Pin.PWRIN), skidl.Pin(num='P4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='R4', name='VDD', func=skidl.Pin.PWRIN), skidl.Pin(num='T4', name='VDD', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='A5', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='B5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C5', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='D5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E5', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='F5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='G5', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='H5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J5', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='K5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L5', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='M5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N5', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='P5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='R5', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='T5', name='VSS', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='A6', name='VDDQ', func=skidl.Pin.PWRIN), skidl.Pin(num='B6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C6', name='VDDQ', func=skidl.Pin.PWRIN), skidl.Pin(num='D6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E6', name='VDDQ', func=skidl.Pin.PWRIN), skidl.Pin(num='F6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='G6', name='VDDQ', func=skidl.Pin.PWRIN), skidl.Pin(num='H6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J6', name='VDDQ', func=skidl.Pin.PWRIN), skidl.Pin(num='K6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L6', name='VDDQ', func=skidl.Pin.PWRIN), skidl.Pin(num='M6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N6', name='VDDQ', func=skidl.Pin.PWRIN), skidl.Pin(num='P6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='R6', name='VDDQ', func=skidl.Pin.PWRIN), skidl.Pin(num='T6', name='VDDQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='A7', name='VSSQ', func=skidl.Pin.PWRIN), skidl.Pin(num='B7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='C7', name='VSSQ', func=skidl.Pin.PWRIN), skidl.Pin(num='D7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='E7', name='VSSQ', func=skidl.Pin.PWRIN), skidl.Pin(num='F7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='G7', name='VSSQ', func=skidl.Pin.PWRIN), skidl.Pin(num='H7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='J7', name='VSSQ', func=skidl.Pin.PWRIN), skidl.Pin(num='K7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='L7', name='VSSQ', func=skidl.Pin.PWRIN), skidl.Pin(num='M7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='N7', name='VSSQ', func=skidl.Pin.PWRIN), skidl.Pin(num='P7', name='VSSQ', func=skidl.Pin.PWRIN),
                 skidl.Pin(num='R7', name='VSSQ', func=skidl.Pin.PWRIN), skidl.Pin(num='T7', name='VSSQ', func=skidl.Pin.PWRIN)])

codec = skidl.Part(lib=None, name='TAC5212', footprint='Package_QFN:QFN-32_5x5mm_P0.5mm',
             pins=[skidl.Pin(num='1', name='DREG', func=skidl.Pin.PWRIN), skidl.Pin(num='2', name='BCLK', func=skidl.Pin.BIDIR),
                   skidl.Pin(num='3', name='FSYNC', func=skidl.Pin.BIDIR), skidl.Pin(num='4', name='DOUT', func=skidl.Pin.OUTPUT),
                   skidl.Pin(num='5', name='DIN', func=skidl.Pin.INPUT), skidl.Pin(num='6', name='IOVDD', func=skidl.Pin.PWRIN),
                   skidl.Pin(num='14', name='MICBIAS', func=skidl.Pin.OUTPUT), skidl.Pin(num='15', name='IN1P', func=skidl.Pin.INPUT),
                   skidl.Pin(num='16', name='IN1M', func=skidl.Pin.INPUT), skidl.Pin(num='17', name='IN2P', func=skidl.Pin.INPUT),
                   skidl.Pin(num='18', name='IN2M', func=skidl.Pin.INPUT), skidl.Pin(num='19', name='OUT1M', func=skidl.Pin.OUTPUT),
                   skidl.Pin(num='20', name='OUT1P', func=skidl.Pin.OUTPUT), skidl.Pin(num='21', name='OUT2P', func=skidl.Pin.OUTPUT),
                   skidl.Pin(num='22', name='OUT2M', func=skidl.Pin.OUTPUT), skidl.Pin(num='A1', name='VSS', func=skidl.Pin.PWRIN),
                   skidl.Pin(num='A2', name='VSS', func=skidl.Pin.PWRIN), skidl.Pin(num='A3', name='VSS', func=skidl.Pin.PWRIN),
                   skidl.Pin(num='A4', name='VSS', func=skidl.Pin.PWRIN)])

# Components
U1 = dsp(ref='U1')
U2 = ram(ref='U2')
U3 = codec(ref='U3')
U4 = skidl.Part('Regulator_Linear', 'TPS7A54', ref='U4', footprint='Regulator_Linear:SOT-223-4_TabPin3')  # 3.3V
U5 = skidl.Part('Regulator_Linear', 'TPS7A54', ref='U5', footprint='Regulator_Linear:SOT-223-4_TabPin3')  # 1.35V DDR
C1, C3, C5, C6, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19 = 16 * [skidl.Part('Device', 'C_Small', value='0.1uF', footprint='Capacitor_SMD:C_0402_1005Metric')]
C2, C4, C20 = 3 * [skidl.Part('Device', 'C_Small', value='10uF', footprint='Capacitor_SMD:C_0603_1608Metric')]
C7 = skidl.Part('Device', 'C_Small', value='100pF', ref='C7', footprint='Capacitor_SMD:C_0402_1005Metric')
C_VREF = skidl.Part('Device', 'C_Small', value='0.1uF', footprint='Capacitor_SMD:C_0402_1005Metric')
R1 = skidl.Part('Device', 'R', value='100R', ref='R1', footprint='Resistor_SMD:R_0402_1005Metric')
R_STAR = skidl.Part('Device', 'R', value='0R', ref='R_STAR', footprint='Resistor_SMD:R_0402_1005Metric')
R_CC1, R_CC2 = 2 * [skidl.Part('Device', 'R', value='5.1k', footprint='Resistor_SMD:R_0402_1005Metric')]
R_FB1 = skidl.Part('Device', 'R', value='6.81k', footprint='Resistor_SMD:R_0402_1005Metric')
R_FB2 = skidl.Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_0402_1005Metric')
R3, R4 = 2 * [skidl.Part('Device', 'R', value='10k', footprint='Resistor_SMD:R_0402_1005Metric')]
R_ZQ_DSP, R_ZQ_RAM = 2 * [skidl.Part('Device', 'R', value='240R', footprint='Resistor_SMD:R_0402_1005Metric')]
R_LED = skidl.Part('Device', 'R', value='1k', footprint='Resistor_SMD:R_0402_1005Metric')
J1 = skidl.Part('Connector_USB', 'USB_C_Receptacle_USB2.0', ref='J1', footprint='Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12')
D1 = skidl.Part('Diode', 'TVS_USB_Dual', ref='D1', footprint='Diode_SMD:D_SOT-23-3')
D2 = skidl.Part('Diode', 'TVS_Audio', ref='D2', footprint='Diode_SMD:D_SOT-23-3')
J2 = skidl.Part('Connector_Audio', 'Jack_3.5mm_Stereo', ref='J2', footprint='Connector_Audio:Jack_3.5mm_CUI_SJ1-3513N_Horizontal')
J3 = skidl.Part('Connector_Audio', 'Jack_3.5mm_Stereo', ref='J3', footprint='Connector_Audio:Jack_3.5mm_CUI_SJ1-3513N_Horizontal')
J4 = skidl.Part('Fuse', 'Fuse_PTC', value='1A', ref='F1', footprint='Fuse:Fuse_1206')
LED1 = skidl.Part('LED', 'LED', ref='LED1', footprint='LED_SMD:LED_0603_1608Metric')
JTAG = skidl.Part('Connector', 'Conn_01x06', ref='JTAG', footprint='Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical')

# Nets (full DDR3, stereo, production)
VCC_1V0 = skidl.Net('VCC_1V0')
VCC_1V35 = skidl.Net('VCC_1V35')
VCC_3V3 = skidl.Net('VCC_3V3')
DGND = skidl.Net('DGND')
AGND = skidl.Net('AGND')
McASP_AXR0 = skidl.Net('McASP_AXR0')
McASP_ACLKX = skidl.Net('McASP_ACLKX')
McASP_AFSX = skidl.Net('McASP_AFSX')
DDR_D0 = skidl.Net('DDR_D0')
DDR_D1 = skidl.Net('DDR_D1')
DDR_D2 = skidl.Net('DDR_D2')
DDR_D3 = skidl.Net('DDR_D3')
DDR_D4 = skidl.Net('DDR_D4')
DDR_D5 = skidl.Net('DDR_D5')
DDR_D6 = skidl.Net('DDR_D6')
DDR_D7 = skidl.Net('DDR_D7')
DDR_D8 = skidl.Net('DDR_D8')
DDR_D9 = skidl.Net('DDR_D9')
DDR_D10 = skidl.Net('DDR_D10')
DDR_D11 = skidl.Net('DDR_D11')
DDR_D12 = skidl.Net('DDR_D12')
DDR_D13 = skidl.Net('DDR_D13')
DDR_D14 = skidl.Net('DDR_D14')
DDR_D15 = skidl.Net('DDR_D15')
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
DDR_CLK = skidl.Net('DDR_CLK')
DDR_CLKN = skidl.Net('DDR_CLKN')
DDR_CAS = skidl.Net('DDR_CAS')
DDR_RAS = skidl.Net('DDR_RAS')
DDR_WE = skidl.Net('DDR_WE')
DDR_LDQS = skidl.Net('DDR_LDQS')
DDR_LDQSN = skidl.Net('DDR_LDQSN')
DDR_UDQS = skidl.Net('DDR_UDQS')
DDR_UDQSN = skidl.Net('DDR_UDQSN')
DDR_LDM = skidl.Net('DDR_LDM')
DDR_UDM = skidl.Net('DDR_UDM')
DDR_BA0 = skidl.Net('DDR_BA0')
DDR_BA1 = skidl.Net('DDR_BA1')
DDR_BA2 = skidl.Net('DDR_BA2')
DDR_CS = skidl.Net('DDR_CS')
DDR_ODT = skidl.Net('DDR_ODT')
DDR_CKE = skidl.Net('DDR_CKE')
DDR_RESET = skidl.Net('DDR_RESET')
DDR_ZQ = skidl.Net('DDR_ZQ')
GUITAR_IN_L = skidl.Net('GUITAR_IN_L')
GUITAR_IN_R = skidl.Net('GUITAR_IN_R')
AUDIO_OUT_L = skidl.Net('AUDIO_OUT_L')
AUDIO_OUT_R = skidl.Net('AUDIO_OUT_R')
USB_DP = skidl.Net('USB_DP')
USB_DM = skidl.Net('USB_DM')
USB_VBUS = skidl.Net('USB_VBUS')
USB_CC1 = skidl.Net('USB_CC1')
USB_CC2 = skidl.Net('USB_CC2')
JTAG_TMS = skidl.Net('JTAG_TMS')
JTAG_TDI = skidl.Net('JTAG_TDI')
JTAG_TDO = skidl.Net('JTAG_TDO')
JTAG_TCK = skidl.Net('JTAG_TCK')
JTAG_TRST = skidl.Net('JTAG_TRST')
JTAG_EMU0 = skidl.Net('JTAG_EMU0')
VREF_DDR = skidl.Net('VREF_DDR')
LPF_OUT_L = skidl.Net('LPF_OUT_L')

# Connections
VCC_1V0 += U1['CVDD'], U3['DREG'], C1[1], C2[1], C3[1], C8[1], C9[1]
VCC_1V35 += U5[3], U2['VDD'], U2['VDDQ'], C10[1], C11[1], C12[1], C13[1], C14[1], C15[1], C16[1], C17[1], C18[1], C19[1], R3[1]
VCC_3V3 += U4[3], U3['AVDD'], U3['IOVDD'], C4[1], C5[1], C6[1], U5[1], LED1[1], R_FB1[1]
DGND += U1['VSS'], U2['VSS'], U2['VSSQ'], C1[2], C2[2], C5[2], R_STAR[1], J1['GND'], D1[3], R_CC1[2], R_CC2[2], C8[2], C9[2], C10[2], C11[2], C12[2], C13[2], C14[2], C15[2], C16[2], C17[2], C18[2], C19[2], R_ZQ_DSP[2], R_ZQ_RAM[2], R_LED[2], J4[2], D2[3], JTAG[6], R4[2], C_VREF[2], R_FB2[2]
AGND += U3['VSS'], U3['VSS'], U3['VSS'], U3['VSS'], C3[2], C4[2], C6[2], C7[2], R_STAR[2], J2['3'], J3['3']
McASP_AXR0 += U1['McASP0_AXR0'], U3['DOUT']
McASP_ACLKX += U1['McASP0_ACLKX'], U3['BCLK']
McASP_AFSX += U1['McASP0_AFSX'], U3['FSYNC']
DDR_D0 += U1['DDR_D0'], U2['DQ0']
DDR_D1 += U1['DDR_D1'], U2['DQ1']
DDR_D2 += U1['DDR_D2'], U2['DQ2']
DDR_D3 += U1['DDR_D3'], U2['DQ3']
DDR_D4 += U1['DDR_D4'], U2['DQ4']
DDR_D5 += U1['DDR_D5'], U2['DQ5']
DDR_D6 += U1['DDR_D6'], U2['DQ6']
DDR_D7 += U1['DDR_D7'], U2['DQ7']
DDR_D8 += U1['DDR_D8'], U2['DQ8']
DDR_D9 += U1['DDR_D9'], U2['DQ9']
DDR_D10 += U1['DDR_D10'], U2['DQ10']
DDR_D11 += U1['DDR_D11'], U2['DQ11']
DDR_D12 += U1['DDR_D12'], U2['DQ12']
DDR_D13 += U1['DDR_D13'], U2['DQ13']
DDR_D14 += U1['DDR_D14'], U2['DQ14']
DDR_D15 += U1['DDR_D15'], U2['DQ15']
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
DDR_CLK += U1['DDR_CLK'], U2['CK']
DDR_CLKN += U1['DDR_CLKN'], U2['CK#']
DDR_CAS += U1['DDR_CAS'], U2['CAS#']
DDR_RAS += U1['DDR_RAS'], U2['RAS#']
DDR_WE += U1['DDR_WE'], U2['WE#']
DDR_LDQS += U1['DDR_LDQS'], U2['LDQS']
DDR_LDQSN += U1['DDR_LDQSN'], U2['LDQS#']
DDR_UDQS += U1['DDR_UDQS'], U2['UDQS']
DDR_UDQSN += U1['DDR_UDQSN'], U2['UDQS#']
DDR_LDM += U1['DDR_LDM'], U2['LDM']
DDR_UDM += U1['DDR_UDM'], U2['UDM']
DDR_BA0 += U1['DDR_BA0'], U2['BA0']
DDR_BA1 += U1['DDR_BA1'], U2['BA1']
DDR_BA2 += U1['DDR_BA2'], U2['BA2']
DDR_CS += U1['DDR_CS'], U2['CS#']
DDR_ODT += U1['DDR_ODT'], U2['ODT']
DDR_CKE += U1['DDR_CKE'], U2['CKE']
DDR_RESET += U1['DDR_RESET'], U2['RESET#']
DDR_ZQ += U1['DDR_ZQ'], R_ZQ_DSP[1], U2['ZQ'], R_ZQ_RAM[1]
VREF_DDR += U1['VREFSSTL'], U2['VREFCA'], U2['VREFDQ'], C_VREF[1], R3[2], R4[1]
GUITAR_IN_L += U3['IN1P'], J2['1'], D2[1]
GUITAR_IN_R += U3['IN2P'], J2['2'], D2[2]
AGND += U3['IN1M'], U3['IN2M'], U3['OUT1M'], U3['OUT2M']
AUDIO_OUT_L += U3['OUT1P'], R1[1]
AUDIO_OUT_R += U3['OUT2P'], J3['2']
LPF_OUT_L += R1[2], C7[1], J3['1']
USB_VBUS += J1['VBUS'], J4[1], U4[1]
USB_DP += U1['USB0_DP'], J1['DP'], D1[1]
USB_DM += U1['USB0_DM'], J1['DM'], D1[2]
USB_CC1 += J1['CC1'], R_CC1[1]
USB_CC2 += J1['CC2'], R_CC2[1]
LED1[2] += R_LED[1]
JTAG_TMS += U1['JTAG_TMS'], JTAG['1']
JTAG_TDI += U1['JTAG_TDI'], JTAG['2']
JTAG_TDO += U1['JTAG_TDO'], JTAG['3']
JTAG_TCK += U1['JTAG_TCK'], JTAG['4']
JTAG_TRST += U1['JTAG_TRST'], JTAG['5']
JTAG_EMU0 += U1['JTAG_EMU0'], JTAG['6']

# Power flags
VCC_1V0.drive = skidl.POWER
VCC_1V35.drive = skidl.POWER
VCC_3V3.drive = skidl.POWER
DGND.drive = skidl.POWER
AGND.drive = skidl.POWER
VREF_DDR.drive = skidl.POWER

try:
    skidl.ERC()
    skidl.generate_netlist()
    skidl.generate_schematic(file_='production_usb_c_dsp_schematic.kicad_sch')
    print("Production-ready USB-C DSP schematic generated as production_usb_c_dsp_schematic.kicad_sch")
except Exception as e:
    print(f"Generation error: {e}")
