# Arduino IoT Monitoring System

## Project Overview
A dual-Arduino system for monitoring voltage and temperature with real-time display, data logging, and predictive analytics.

## System Architecture

### Hardware Components
- **Arduino UNO #1**: Display Unit (LCD + Sensors)
- **Arduino UNO #2**: Data Logger (Sensors + Serial Communication)
- **Sensors**: Voltage sensor, Temperature sensor
- **Display**: LCD for real-time readings

### Software Components
- **Arduino Code**: Sensor reading and display/communication
- **Python Application**: 3-page GUI for data visualization and prediction

## Project Structure
```
├── arduino/
│   ├── display_unit/          # Arduino #1 code
│   └── data_logger/           # Arduino #2 code
├── python_app/
│   ├── main.py               # Main application
│   ├── pages/                # GUI pages
│   ├── data/                 # Data storage
│   └── prediction/           # ML prediction system
└── docs/                     # Documentation
```

## Features
- Real-time sensor monitoring
- Historical data analysis
- Predictive analytics
- Serial communication
- LCD display interface#