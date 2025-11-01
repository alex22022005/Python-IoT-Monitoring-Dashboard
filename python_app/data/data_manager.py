"""
Data Manager for handling Arduino serial communication and data storage
"""

import serial
import json
import sqlite3
import threading
import time
from datetime import datetime
from typing import List, Dict, Optional

class DataManager:
    def __init__(self, port='COM5', baudrate=9600, db_path=None):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.is_collecting = False
        self.latest_data = {'voltage': 0.0, 'temperature': 0.0, 'current': 0.0, 'timestamp': None}
        self.status_callback = None
        
        # Set up proper paths for executable
        self.setup_data_paths(db_path)
        
        # Initialize database and CSV storage
        self.init_database()
        self.init_csv_storage()
    
    def setup_data_paths(self, db_path=None):
        """Setup proper data paths for both script and executable modes"""
        import os
        import sys
        
        # Get the directory where the executable or script is located
        if hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller bundle - use directory where .exe is located
            base_dir = os.path.dirname(sys.executable)
        else:
            # Running as script - use current directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.join(base_dir, '..')  # Go up to project root
        
        # Create IoT_Data directory for all data files
        self.data_dir = os.path.join(base_dir, 'IoT_Data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
        
        # Set database path
        if db_path is None:
            self.db_path = os.path.join(self.data_dir, 'sensor_data.db')
        else:
            self.db_path = db_path
        
        print(f"📁 Data directory: {self.data_dir}")
        print(f"🗄️ Database path: {self.db_path}")
    
    def scan_ports(self):
        """Scan for available COM ports"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            available_ports = []
            
            print("Scanning for available COM ports...")
            for port in ports:
                try:
                    # Try to open each port briefly to check availability
                    test_serial = serial.Serial(port.device, self.baudrate, timeout=0.1)
                    test_serial.close()
                    available_ports.append(port.device)
                    print(f"  ✓ {port.device} - {port.description} (Available)")
                except:
                    print(f"  ✗ {port.device} - {port.description} (Busy)")
            
            return available_ports
        except ImportError:
            print("serial.tools.list_ports not available")
            return []
    
    def auto_connect(self):
        """Try to automatically connect to an available Arduino"""
        available_ports = self.scan_ports()
        
        if not available_ports:
            print("No available COM ports found!")
            return False
        
        # Try each available port
        for port in available_ports:
            print(f"Trying to connect to {port}...")
            self.port = port
            if self.connect_arduino():
                return True
        
        print("Could not connect to any available port")
        return False
    
    def init_database(self):
        """Initialize SQLite database for storing sensor data"""
        import os
        
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                voltage REAL NOT NULL,
                temperature REAL NOT NULL,
                current REAL NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def init_csv_storage(self):
        """Initialize CSV file for data storage with proper executable path handling"""
        import os
        from datetime import datetime
        
        # CSV file path with current date in the data directory
        today = datetime.now().strftime('%Y-%m-%d')
        self.csv_path = os.path.join(self.data_dir, f'sensor_data_{today}.csv')
        self.csv_dir = self.data_dir  # Store directory path for folder opening
        
        # Create CSV file with headers if it doesn't exist
        if not os.path.exists(self.csv_path):
            import csv
            with open(self.csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['timestamp', 'voltage', 'current', 'temperature', 'power'])
                print(f"📄 Created CSV file: {self.csv_path}")
        
        print(f"💾 CSV data will be saved to: {self.csv_path}")
    
    def register_status_callback(self, callback):
        """Register callback for connection status updates"""
        self.status_callback = callback
    
    def update_status(self, status, message=""):
        """Update connection status"""
        if self.status_callback:
            self.status_callback(status, message)
    
    def connect_arduino(self) -> bool:
        """Establish serial connection with Arduino"""
        self.update_status("connecting", "Connecting to Arduino...")
        
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"✓ Connected to Arduino on {self.port}")
            self.update_status("connected", f"Connected to {self.port}")
            return True
        except serial.SerialException as e:
            if "PermissionError" in str(e) or "Access is denied" in str(e):
                print(f"✗ Port {self.port} is busy!")
                print("  Troubleshooting steps:")
                print("  1. Close Arduino IDE Serial Monitor")
                print("  2. Close any other serial terminal programs")
                print("  3. Disconnect and reconnect Arduino USB cable")
                print("  4. Try a different COM port")
                self.update_status("error", f"Port {self.port} busy")
            else:
                print(f"✗ Serial connection error: {e}")
                print("  Check if Arduino is connected and drivers are installed")
                self.update_status("error", "Connection failed")
            return False
        except Exception as e:
            print(f"✗ Failed to connect to Arduino: {e}")
            self.update_status("error", "Connection error")
            return False
    
    def start_collection(self):
        """Start collecting data from Arduino"""
        print("🚀 Starting data collection system...")
        self.is_collecting = True
        
        # Try to connect to the specified port first
        if not self.connect_arduino():
            print(f"Retrying with auto-detection...")
            if not self.auto_connect():
                print("Could not establish Arduino connection. Running in demo mode...")
                print("You can plug in Arduino anytime - the system will auto-detect it!")
                self.start_demo_mode()
                return
        
        # Start real Arduino data collection
        self.start_real_collection()
    
    def parse_arduino_csv(self, line: str) -> Optional[Dict]:
        """Parse Arduino CSV format: V:4.85,C:1.23,T:24.5"""
        try:
            # Split by comma and parse each part
            parts = line.split(',')
            data = {}
            
            for part in parts:
                part = part.strip()
                if ':' in part:
                    key, value = part.split(':', 1)
                    if key == 'V':
                        data['voltage'] = float(value)
                    elif key == 'C':
                        data['current'] = float(value)
                    elif key == 'T':
                        data['temperature'] = float(value)
            
            # Ensure all required fields are present
            if 'voltage' in data and 'current' in data and 'temperature' in data:
                return data
            else:
                return None
                
        except Exception as e:
            print(f"Error parsing Arduino CSV: {e}")
            return None
    
    def get_csv_file_path(self):
        """Get the current CSV file path"""
        return self.csv_path
    
    def get_csv_directory(self):
        """Get the CSV directory path for opening in file explorer"""
        # Always return the data_dir (IoT_Data folder) where CSV files are stored
        return self.data_dir
    
    def get_csv_info(self):
        """Get information about the CSV file"""
        try:
            import os
            if os.path.exists(self.csv_path):
                size = os.path.getsize(self.csv_path)
                # Count lines (subtract 1 for header)
                with open(self.csv_path, 'r') as f:
                    line_count = sum(1 for line in f) - 1
                
                return {
                    'path': self.csv_path,
                    'size_bytes': size,
                    'size_kb': round(size / 1024, 2),
                    'record_count': line_count,
                    'exists': True
                }
            else:
                return {
                    'path': self.csv_path,
                    'exists': False
                }
        except Exception as e:
            print(f"Error getting CSV info: {e}")
            return {'exists': False, 'error': str(e)}
    
    def process_data(self, data: Dict, is_demo: bool = False):
        """Process incoming data and store in database"""
        try:
            voltage = float(data.get('voltage', 0))
            temperature = float(data.get('temperature', 0))
            current = float(data.get('current', 0))
            timestamp = datetime.now()
            
            # Check if data is valid (not all zeros or inactive)
            is_valid_data = not (voltage == 0 and current == 0 and temperature == 0)
            
            # Update latest data (always update for GUI display)
            self.latest_data = {
                'voltage': voltage,
                'temperature': temperature,
                'current': current,
                'timestamp': timestamp
            }
            
            # Only store data if it's valid (not all zeros)
            if is_valid_data:
                # Store in database
                self.store_data(voltage, temperature, current, timestamp)
                
                # Store in CSV file only for real data (not demo data)
                if not is_demo:
                    self.store_csv_data(voltage, current, temperature, timestamp)
                    print(f"📊 Real Data: V={voltage:.2f}V, C={current:.2f}A, T={temperature:.1f}°C")
                else:
                    print(f"🎭 Demo Data: V={voltage:.2f}V, C={current:.2f}A, T={temperature:.1f}°C")
            else:
                print(f"⚠️  Skipping inactive data (all zeros)")
            
        except Exception as e:
            print(f"Error processing data: {e}")
    
    def start_demo_mode(self):
        """Start demo mode with simulated data when Arduino is not available"""
        import random
        import math
        
        print("🎭 Starting DEMO MODE - Generating simulated sensor data")
        print("   (This allows you to test the GUI without Arduino)")
        print("   💡 Plug in Arduino anytime - system will auto-detect and switch!")
        self.update_status("demo", "Demo mode - plug Arduino to switch")
        
        self.is_collecting = True
        start_time = time.time()
        last_arduino_check = 0
        
        while self.is_collecting:
            try:
                current_time = time.time()
                
                # Check for Arduino every 5 seconds
                if current_time - last_arduino_check > 5:
                    print("🔍 Checking for Arduino connection...")
                    if self.auto_connect():
                        print("🎉 Arduino detected! Switching from demo mode to real data...")
                        self.start_real_collection()
                        return
                    last_arduino_check = current_time
                
                # Generate realistic simulated data
                elapsed = current_time - start_time
                
                # Base values with slow trends
                base_voltage = 4.2 + 0.3 * math.sin(elapsed / 60)  # 1-minute cycle
                base_current = 1.0 + 0.4 * math.sin(elapsed / 45)  # 45-second cycle
                base_temp = 22.0 + 2.0 * math.sin(elapsed / 120)   # 2-minute cycle
                
                # Add noise and variations
                voltage = base_voltage + random.uniform(-0.2, 0.2)
                current = base_current + random.uniform(-0.15, 0.15)
                temperature = base_temp + random.uniform(-0.5, 0.5) + (current - 1.0) * 2  # Current affects temp
                
                # Clamp to realistic ranges
                voltage = max(3.0, min(5.2, voltage))
                current = max(0.1, min(2.5, current))
                temperature = max(18.0, min(35.0, temperature))
                
                # Create data dictionary
                data = {
                    'voltage': voltage,
                    'current': current,
                    'temperature': temperature
                }
                
                # Process the simulated data (mark as demo data)
                self.process_data(data, is_demo=True)
                
                # Wait 1 second (same as Arduino)
                time.sleep(1.0)
                
            except Exception as e:
                print(f"Error in demo mode: {e}")
                time.sleep(1)
    
    def start_real_collection(self):
        """Start collecting real data from Arduino"""
        print("📡 Starting real Arduino data collection...")
        self.update_status("connected", "Collecting real data")
        
        while self.is_collecting:
            try:
                if self.serial_connection and self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8').strip()
                    
                    # Handle both JSON format and CSV format from Arduino
                    if line.startswith('{') and line.endswith('}'):
                        # JSON format (original)
                        try:
                            data = json.loads(line)
                            self.process_data(data, is_demo=False)
                        except json.JSONDecodeError:
                            print(f"Invalid JSON: {line}")
                    elif line.startswith('V:') and 'C:' in line and 'T:' in line:
                        # CSV format from Arduino test generator: "V:4.85,C:1.23,T:24.5"
                        try:
                            data = self.parse_arduino_csv(line)
                            if data:
                                self.process_data(data, is_demo=False)
                        except Exception as e:
                            print(f"Error parsing Arduino CSV: {line} - {e}")
                    elif not line.startswith('#'):  # Ignore debug messages starting with #
                        # Try to parse as simple CSV: voltage,current,temperature
                        try:
                            parts = line.split(',')
                            if len(parts) == 3:
                                data = {
                                    'voltage': float(parts[0]),
                                    'current': float(parts[1]),
                                    'temperature': float(parts[2])
                                }
                                self.process_data(data, is_demo=False)
                        except (ValueError, IndexError):
                            if line.strip():  # Only print non-empty lines
                                print(f"Unrecognized data format: {line}")
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                print(f"Error reading Arduino data: {e}")
                print("🔌 Arduino disconnected! Switching back to demo mode...")
                self.serial_connection = None
                self.start_demo_mode()
                return
    
    def store_data(self, voltage: float, temperature: float, current: float, timestamp: datetime):
        """Store data in SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sensor_readings (timestamp, voltage, temperature, current)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, voltage, temperature, current))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error storing data: {e}")
    
    def store_csv_data(self, voltage: float, current: float, temperature: float, timestamp: datetime):
        """Store data in CSV file"""
        try:
            import csv
            
            # Calculate power
            power = voltage * current
            
            # Append data to CSV file
            with open(self.csv_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    f"{voltage:.2f}",
                    f"{current:.2f}",
                    f"{temperature:.1f}",
                    f"{power:.2f}"
                ])
            
        except Exception as e:
            print(f"Error storing CSV data: {e}")
    
    def get_latest_data(self) -> Dict:
        """Get the most recent sensor reading"""
        return self.latest_data.copy() if self.latest_data else {
            'voltage': 0.0, 'current': 0.0, 'temperature': 0.0, 'timestamp': None
        }
    
    def get_historical_data(self, limit: int = 100) -> List[Dict]:
        """Get historical data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, voltage, temperature, current 
                FROM sensor_readings 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'timestamp': row[0],
                    'voltage': row[1],
                    'temperature': row[2],
                    'current': row[3]
                }
                for row in rows
            ]
            
        except Exception as e:
            print(f"Error retrieving historical data: {e}")
            return []
    
    def stop_collection(self):
        """Stop data collection"""
        self.is_collecting = False
        if self.serial_connection:
            self.serial_connection.close()