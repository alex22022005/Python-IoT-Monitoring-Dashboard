# Setup Guide

## Hardware Setup

### Arduino Display Unit (Arduino #1)

1. Connect LCD display:

   - VSS to GND
   - VDD to 5V
   - V0 to potentiometer (contrast adjustment)
   - RS to pin 12
   - Enable to pin 11
   - D4 to pin 5
   - D5 to pin 4
   - D6 to pin 3
   - D7 to pin 2

2. Connect sensors:
   - Voltage sensor to A0
   - Temperature sensor (LM35) to A1
   - Current sensor (ACS712) to A2

### Arduino Data Logger (Arduino #2)

1. Connect sensors (same as Display Unit):

   - Voltage sensor to A0
   - Temperature sensor (LM35) to A1
   - Current sensor (ACS712) to A2

2. Connect USB cable to laptop for serial communication

## Software Setup

### Arduino IDE

1. Install Arduino IDE
2. Upload `display_unit.ino` to Arduino #1
3. Upload `data_logger.ino` to Arduino #2

### Python Environment

1. Install Python 3.8+
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Update COM port in `data_manager.py` (default: COM3)
2. Adjust sensor calibration values in Arduino code if needed

## Running the System

1. Power on both Arduino units
2. Connect Arduino #2 to laptop via USB
3. Run Python application:
   ```bash
   python main.py
   ```

## Troubleshooting

### Common Issues

- **Serial connection failed**: Check COM port and ensure Arduino is connected
- **No data received**: Verify Arduino code is uploaded and running
- **LCD not displaying**: Check wiring and contrast adjustment
- **Incorrect readings**: Calibrate sensor values in Arduino code

### Sensor Calibration

- **Voltage sensor**: Adjust multiplier in `readVoltage()` function
- **Temperature sensor**: Verify LM35 connections and scaling factor
