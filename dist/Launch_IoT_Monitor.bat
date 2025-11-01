@echo off
title IoT Monitoring System - Final Version
color 0A

echo ===============================================
echo         IoT Monitoring System v1.0
echo ===============================================
echo.
echo 🚀 Professional IoT Monitoring Application
echo.
echo ✅ FEATURES:
echo 📊 Real-time sensor monitoring (Live Data)
echo 📈 Historical data analysis (Past Data) 
echo 🔮 Machine learning predictions (Predictions)
echo 🌙 Dark/Light theme toggle
echo 📁 CSV export with folder access
echo 🔌 Arduino auto-detection with demo mode
echo.
echo 💾 DATA STORAGE:
echo All data saved in "IoT_Data" folder next to this executable
echo - CSV files: sensor_data_YYYY-MM-DD.csv
echo - Database: sensor_data.db
echo.
echo 🎯 READY TO USE:
echo - Works with or without Arduino hardware
echo - Demo mode for testing and presentations
echo - Professional interface with responsive design
echo.
echo Press any key to launch IoT Monitor...
pause >nul

echo.
echo 🚀 Starting IoT Monitoring System...
start "" "IoT_Monitor_Titles_Fixed.exe"

echo.
echo ✅ Application launched successfully!
echo.
echo 💡 Tips:
echo - Toggle theme with the Dark/Light Mode button
echo - Use "Open Folder" in Past Data to access CSV files
echo - All features work in demo mode without hardware
echo.
echo This window will close in 3 seconds...
timeout /t 3 >nul