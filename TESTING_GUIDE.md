# IoT Monitoring System - Testing Guide

This guide will help you test the complete IoT monitoring system using a single Arduino UNO generating random sensor data.

## 🔧 Hardware Setup

### Required Components
- 1x Arduino UNO
- 1x USB Cable
- Computer with Python and Arduino IDE

### Arduino Setup
1. **Connect Arduino UNO** to your computer via USB
2. **Open Arduino IDE**
3. **Load the test sketch**: `arduino/test_data_generator/test_data_generator.ino`
4. **Select your board**: Tools → Board → Arduino UNO
5. **Select COM port**: Tools → Port → (your Arduino's port)
6. **Upload the sketch**

### Verify Arduino Operation
1. **Open Serial Monitor** (Tools → Serial Monitor)
2. **Set baud rate** to 9600
3. **You should see**:
   ```
   IoT Monitoring System - Test Data Generator
   Arduino UNO Ready - Generating Random Sensor Data
   Data Format: V:voltage,C:current,T:temperature
   ----------------------------------------
   V:4.23,C:1.15,T:22.3
   V:4.18,C:1.22,T:22.5
   ```

## 🐍 Python Setup

### Install Dependencies
```bash
cd python_app
pip install -r requirements.txt
```

### Test Arduino Connection
1. **Close Arduino Serial Monitor** (important!)
2. **Run connection test**:
   ```bash
   python test_connection.py
   ```
3. **Expected output**:
   ```
   Testing Arduino connection on COM3 at 9600 baud...
   ✓ Connected to Arduino on COM3
   Waiting for data...
   
   [14:23:15] #  1 | Voltage:  4.23V | Current:  1.15A | Temperature:  22.3°C
   [14:23:16] #  2 | Voltage:  4.18V | Current:  1.22A | Temperature:  22.5°C
   ```

### Update COM Port (if needed)
If your Arduino is on a different port:

1. **Check available ports** in the test output
2. **Update data_manager.py**:
   ```python
   # Line ~11 in python_app/data/data_manager.py
   def __init__(self, port='COM4', baudrate=9600, db_path='data/db/sensor_data.db'):
   ```

## 🚀 Run the Complete Application

### Start the GUI Application
```bash
cd python_app
python main.py
```

### Expected Behavior

#### 1. **Live Data Page**
- Real-time charts updating every second
- Current readings display showing:
  - Voltage: 3.0V - 5.2V
  - Current: 0.1A - 2.5A
  - Temperature: 18°C - 35°C
  - Power: Calculated (V × C)

#### 2. **Past Data Page**
- Historical charts with trend lines
- Statistics showing min/max/average values
- Export functionality for CSV data

#### 3. **Predictions Page**
- AI predictions based on historical data
- Model accuracy metrics (R² scores)
- Future trend visualization

#### 4. **Dark/Light Mode Toggle**
- **🌙 Dark Mode** button (in light mode)
- **☀️ Light Mode** button (in dark mode)
- Instant theme switching across all pages

## 🎨 Testing Features

### Theme Toggle
1. Click the theme button in the top-right corner
2. Verify all pages switch themes instantly
3. Check that charts, text, and UI elements update properly

### Data Visualization
1. **Live Data**: Watch real-time updates
2. **Past Data**: Use dropdown to change data range (50, 100, 500, 1000, All)
3. **Predictions**: Try different prediction horizons (1, 6, 12, 24, 48, 72 hours)

### Data Export
1. Go to **Past Data** page
2. Click **Export CSV** button
3. Save data to verify database functionality

## 🔍 Troubleshooting

### Arduino Issues

**No data in Serial Monitor:**
- Check USB connection
- Verify correct COM port selection
- Ensure sketch uploaded successfully
- Try pressing Arduino reset button

**LED not blinking:**
- Check if sketch uploaded correctly
- Verify Arduino is powered (LED should blink on startup)

### Python Issues

**"Port not found" error:**
- Close Arduino Serial Monitor
- Check COM port in `data_manager.py`
- Run `test_connection.py` to verify port

**"Module not found" error:**
- Install requirements: `pip install -r requirements.txt`
- Ensure you're in the `python_app` directory

**No data in GUI:**
- Verify Arduino is sending data (run `test_connection.py`)
- Check database creation in `data/db/` folder
- Look for error messages in console

**Charts not updating:**
- Check if data is being received (console output)
- Verify matplotlib installation
- Try refreshing data on Past Data page

### Performance Issues

**Slow GUI response:**
- Reduce data collection frequency in Arduino code
- Limit historical data range in Past Data page
- Close other applications using serial ports

**Memory usage:**
- Database automatically manages old data
- Restart application if memory usage grows

## 📊 Data Characteristics

The Arduino generates realistic sensor data:

### Voltage (V)
- **Range**: 3.0V - 5.2V
- **Typical**: ~4.2V (USB supply)
- **Variations**: Power fluctuations, noise

### Current (C)
- **Range**: 0.1A - 2.5A  
- **Typical**: ~1.0A (moderate load)
- **Patterns**: Load cycles, correlates with temperature

### Temperature (T)
- **Range**: 18°C - 35°C
- **Typical**: ~22°C (room temperature)
- **Effects**: Influenced by current (thermal heating)

## 🎯 Success Criteria

Your system is working correctly if you see:

✅ **Arduino**: Continuous data transmission every second  
✅ **Connection Test**: Successful data parsing and display  
✅ **Live Data**: Real-time charts updating smoothly  
✅ **Past Data**: Historical analysis with statistics  
✅ **Predictions**: ML models generating future trends  
✅ **Theme Toggle**: Instant switching between dark/light modes  
✅ **Database**: Data persistence and export functionality  

## 🚀 Next Steps

Once testing is complete:

1. **Replace Arduino simulation** with real sensors
2. **Customize data ranges** for your specific application
3. **Add more sensors** by extending the data format
4. **Implement alerts** for threshold monitoring
5. **Add data logging** to files or cloud services

Your IoT monitoring system is now ready for real-world deployment!