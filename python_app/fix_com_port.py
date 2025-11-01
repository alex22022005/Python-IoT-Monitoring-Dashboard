"""
COM Port Troubleshooting Tool
Helps identify and fix Arduino connection issues
"""

import serial
import serial.tools.list_ports
import time
import sys

def check_arduino_ide():
    """Check if Arduino IDE might be using the port"""
    import psutil
    
    arduino_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'arduino' in proc.info['name'].lower():
                arduino_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if arduino_processes:
        print("⚠️  Arduino IDE processes detected:")
        for proc in arduino_processes:
            print(f"   - {proc['name']} (PID: {proc['pid']})")
        print("   Please close Arduino IDE Serial Monitor and try again.")
        return True
    return False

def scan_all_ports():
    """Scan and test all COM ports"""
    print("🔍 Scanning all COM ports...")
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("❌ No COM ports found!")
        print("   - Check if Arduino is connected via USB")
        print("   - Try a different USB cable")
        print("   - Check Device Manager for Arduino")
        return []
    
    available_ports = []
    busy_ports = []
    
    for port in ports:
        print(f"\n📍 Testing {port.device}: {port.description}")
        
        try:
            # Try to open the port
            test_serial = serial.Serial(port.device, 9600, timeout=1)
            test_serial.close()
            available_ports.append(port.device)
            print(f"   ✅ Available")
            
        except serial.SerialException as e:
            busy_ports.append((port.device, str(e)))
            if "PermissionError" in str(e) or "Access is denied" in str(e):
                print(f"   🔒 BUSY - Another program is using this port")
            else:
                print(f"   ❌ Error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
    
    return available_ports, busy_ports

def test_arduino_communication(port):
    """Test communication with Arduino on specific port"""
    print(f"\n🔌 Testing Arduino communication on {port}...")
    
    try:
        ser = serial.Serial(port, 9600, timeout=2)
        time.sleep(2)  # Wait for Arduino to initialize
        
        print("   Waiting for data...")
        
        # Try to read some data
        for i in range(10):  # Try for 10 seconds
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"   📨 Received: {line}")
                    
                    # Check if it looks like Arduino data
                    if 'V:' in line and 'C:' in line and 'T:' in line:
                        print("   ✅ Arduino test data detected!")
                        ser.close()
                        return True
                    elif line.startswith('IoT') or line.startswith('Arduino'):
                        print("   ✅ Arduino startup message detected!")
                        ser.close()
                        return True
            
            time.sleep(1)
        
        print("   ⚠️  No recognizable Arduino data received")
        print("   Check if the Arduino sketch is uploaded correctly")
        ser.close()
        return False
        
    except Exception as e:
        print(f"   ❌ Communication test failed: {e}")
        return False

def main():
    """Main troubleshooting function"""
    print("=" * 60)
    print("🔧 Arduino COM Port Troubleshooting Tool")
    print("=" * 60)
    
    # Check for Arduino IDE processes
    print("\n1️⃣ Checking for conflicting processes...")
    if check_arduino_ide():
        print("\n💡 Solution: Close Arduino IDE Serial Monitor and try again")
        return
    else:
        print("   ✅ No Arduino IDE processes detected")
    
    # Scan all ports
    print("\n2️⃣ Scanning COM ports...")
    available_ports, busy_ports = scan_all_ports()
    
    if busy_ports:
        print(f"\n🔒 Busy ports found:")
        for port, error in busy_ports:
            print(f"   - {port}: {error}")
        print("\n💡 Solutions for busy ports:")
        print("   - Close Arduino IDE Serial Monitor")
        print("   - Close any other serial terminal programs")
        print("   - Unplug and reconnect Arduino USB cable")
        print("   - Restart your computer if necessary")
    
    if not available_ports:
        print("\n❌ No available COM ports found!")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Disconnect Arduino USB cable")
        print("   2. Close all Arduino IDE windows")
        print("   3. Wait 5 seconds")
        print("   4. Reconnect Arduino USB cable")
        print("   5. Run this script again")
        return
    
    print(f"\n✅ Available ports: {', '.join(available_ports)}")
    
    # Test Arduino communication on available ports
    print("\n3️⃣ Testing Arduino communication...")
    working_ports = []
    
    for port in available_ports:
        if test_arduino_communication(port):
            working_ports.append(port)
    
    # Results and recommendations
    print("\n" + "=" * 60)
    print("📋 RESULTS & RECOMMENDATIONS")
    print("=" * 60)
    
    if working_ports:
        print(f"✅ Arduino found on: {', '.join(working_ports)}")
        recommended_port = working_ports[0]
        print(f"🎯 Recommended port: {recommended_port}")
        
        print(f"\n📝 Update your Python code:")
        print(f"   In data_manager.py, change the port to: '{recommended_port}'")
        print(f"   Or run: python test_connection.py")
        
    else:
        print("❌ No working Arduino connection found")
        print("\n🔧 Next steps:")
        print("   1. Verify Arduino sketch is uploaded correctly")
        print("   2. Check if Arduino is sending data (open Serial Monitor briefly)")
        print("   3. Try uploading the test_data_generator.ino sketch")
        print("   4. Check USB cable and Arduino power")
    
    print(f"\n🚀 Once fixed, run: python python_app/main.py")

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        print("Installing psutil for process detection...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
    
    main()