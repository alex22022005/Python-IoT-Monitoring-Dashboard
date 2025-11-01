"""
Test script to verify Arduino connection and data reception
Run this before starting the main GUI application
"""

import serial
import time
import sys
from datetime import datetime

def test_arduino_connection(port='COM3', baudrate=9600):
    """Test connection to Arduino and display received data"""
    
    print(f"Testing Arduino connection on {port} at {baudrate} baud...")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Connect to Arduino
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for Arduino to initialize
        
        print(f"✓ Connected to Arduino on {port}")
        print("Waiting for data...\n")
        
        data_count = 0
        start_time = time.time()
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                
                if line:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    
                    # Parse and display data
                    if line.startswith('V:') and 'C:' in line and 'T:' in line:
                        # Parse Arduino CSV format
                        try:
                            parts = line.split(',')
                            voltage = float(parts[0].split(':')[1])
                            current = float(parts[1].split(':')[1])
                            temperature = float(parts[2].split(':')[1])
                            
                            data_count += 1
                            print(f"[{current_time}] #{data_count:3d} | "
                                  f"Voltage: {voltage:5.2f}V | "
                                  f"Current: {current:5.2f}A | "
                                  f"Temperature: {temperature:5.1f}°C")
                            
                        except (ValueError, IndexError) as e:
                            print(f"[{current_time}] Parse error: {line} ({e})")
                    
                    elif line.startswith('#'):
                        # Debug message from Arduino
                        print(f"[{current_time}] Arduino: {line}")
                    
                    elif line.startswith('IoT') or line.startswith('Arduino') or line.startswith('Data Format'):
                        # Startup messages
                        print(f"[{current_time}] Arduino: {line}")
                    
                    else:
                        # Unknown format
                        print(f"[{current_time}] Unknown: {line}")
            
            time.sleep(0.1)
    
    except serial.SerialException as e:
        print(f"✗ Serial connection error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if Arduino is connected")
        print("2. Verify the correct COM port")
        print("3. Ensure Arduino sketch is uploaded")
        print("4. Close Arduino IDE Serial Monitor")
        return False
    
    except KeyboardInterrupt:
        print(f"\n\nTest completed!")
        print(f"Total data points received: {data_count}")
        elapsed = time.time() - start_time
        if elapsed > 0:
            rate = data_count / elapsed
            print(f"Data rate: {rate:.1f} points/second")
        
        ser.close()
        return True
    
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def scan_ports():
    """Scan for available COM ports"""
    import serial.tools.list_ports
    
    print("Scanning for available COM ports...")
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("No COM ports found!")
        return []
    
    print("Available ports:")
    for i, port in enumerate(ports):
        print(f"  {i+1}. {port.device} - {port.description}")
    
    return [port.device for port in ports]

def main():
    """Main test function"""
    print("=" * 60)
    print("IoT Monitoring System - Arduino Connection Test")
    print("=" * 60)
    
    # Scan for ports
    available_ports = scan_ports()
    
    if not available_ports:
        print("No COM ports available. Please connect your Arduino.")
        return
    
    # Default port or let user choose
    if len(available_ports) == 1:
        port = available_ports[0]
        print(f"\nUsing port: {port}")
    else:
        print(f"\nMultiple ports found. Using default: {available_ports[0]}")
        print("To use a different port, modify the 'port' variable in this script.")
        port = available_ports[0]
    
    # Test connection
    print(f"\nStarting connection test...")
    success = test_arduino_connection(port)
    
    if success:
        print("\n✓ Arduino connection test successful!")
        print("You can now run the main Python application.")
    else:
        print("\n✗ Arduino connection test failed!")
        print("Please check the troubleshooting steps above.")

if __name__ == "__main__":
    main()