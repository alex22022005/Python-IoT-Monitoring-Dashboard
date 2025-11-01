# Arduino Test Data Generator

This Arduino sketch generates realistic random sensor data for testing the IoT Monitoring Python application.

## Features

- **Realistic Data Generation**: Simulates voltage, current, and temperature sensors
- **Continuous Transmission**: Sends data every second via Serial (9600 baud)
- **Visual Feedback**: LED blinks when transmitting data
- **Trend Simulation**: Includes realistic long-term trends and correlations
- **Debug Information**: Periodic status updates

## Data Format

The Arduino sends data in this format:
```
V:4.85,C:1.23,T:24.5
```

Where:
- `V:` = Voltage in Volts (3.0V - 5.2V)
- `C:` = Current in Amperes (0.1A - 2.5A)  
- `T:` = Temperature in Celsius (18°C - 35°C)

## Hardware Setup

### Required Components
- 1x Arduino UNO
- 1x USB Cable
- Built-in LED (Pin 13) for status indication

### Connections
No external sensors required! This is a simulation sketch.

## Software Setup

### 1. Upload the Code
1. Open Arduino IDE
2. Load `test_data_generator.ino`
3. Select your Arduino UNO board and COM port
4. Upload the sketch

### 2. Verify Operation
1. Open Serial Monitor (9600 baud)
2. You should see:
   ```
   IoT Monitoring System - Test Data Generator
   Arduino UNO Ready - Generating Random Sensor Data
   Data Format: V:voltage,C:current,T:temperature
   ----------------------------------------
   V:4.23,C:1.15,T:22.3
   V:4.18,C:1.22,T:22.5
   V:4.31,C:1.08,T:22.1
   ```

### 3. Connect to Python App
1. Note the COM port (e.g., COM3, COM4)
2. Update the Python app's serial port configuration
3. Run the Python application

## Data Characteristics

### Voltage (V)
- **Range**: 3.0V to 5.2V
- **Base**: ~4.2V (typical USB/Arduino supply)
- **Variations**: Power supply fluctuations, noise
- **Trends**: Slow changes over time

### Current (C)
- **Range**: 0.1A to 2.5A
- **Base**: ~1.0A (moderate load)
- **Variations**: Load changes, correlates with temperature
- **Patterns**: Sine wave variations simulating load cycles

### Temperature (T)
- **Range**: 18°C to 35°C
- **Base**: ~22°C (room temperature)
- **Variations**: Affected by current (thermal effects)
- **Trends**: Slow ambient temperature changes

## Optional Serial Commands

You can send these commands via Serial Monitor to change simulation parameters:

- `HIGH_LOAD` - Simulate high current scenario
- `LOW_LOAD` - Simulate low current scenario  
- `POWER_FLUC` - Simulate power fluctuations
- `RESET` - Reset to normal parameters
- `STATUS` - Show current base values

## Troubleshooting

### No Data Received
1. Check COM port selection
2. Verify baud rate (9600)
3. Ensure Arduino is powered and sketch uploaded
4. Check USB cable connection

### Python App Not Connecting
1. Close Serial Monitor before running Python app
2. Update COM port in Python configuration
3. Check if port is already in use by another application

### Unrealistic Data
- Data includes intentional noise and variations
- Trends change slowly over time
- Values are constrained to realistic ranges

## Integration with Python App

The Python application expects data in the exact format this Arduino provides:
```python
# Python will parse: "V:4.85,C:1.23,T:24.5"
# Into: voltage=4.85, current=1.23, temperature=24.5
```

Make sure your Python app's serial configuration matches:
- **Baud Rate**: 9600
- **Data Format**: "V:x.xx,C:x.xx,T:xx.x"
- **Update Rate**: 1 second intervals

## LED Status Indicator

- **Startup**: 5 quick blinks
- **Data Transmission**: Brief blink every second
- **Continuous**: Normal operation

This test setup allows you to fully test your Python IoT monitoring application without needing actual sensors!