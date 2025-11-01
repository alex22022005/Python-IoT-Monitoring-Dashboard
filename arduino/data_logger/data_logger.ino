/*
 * Arduino Data Logger Unit
 * Reads sensors and sends data via serial to laptop
 */

#include <DHT.h>

// Pin definitions (matching display unit)
const int voltagePin = A0;   // Analog pin for voltage sensor
const int currentPin = A1;   // Analog pin for current sensor  
const int dht11Pin = 7;      // Digital pin for DHT11

// DHT11 sensor
#define DHT_TYPE DHT11
DHT dht(dht11Pin, DHT_TYPE);

// Variables
float voltage = 0.0;
float temperature = 0.0;
float humidity = 0.0;
float current = 0.0;
unsigned long lastReading = 0;
const unsigned long readingInterval = 5000; // Send data every 5 seconds

void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.println("Arduino Data Logger Ready");
}

void loop() {
  unsigned long currentTime = millis();
  
  if (currentTime - lastReading >= readingInterval) {
    // Read sensors
    voltage = readVoltage();
    current = readCurrent();
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();
    
    // Check for sensor errors
    if (isnan(temperature) || isnan(humidity)) {
      temperature = 0.0;
      humidity = 0.0;
    }
    
    // Send data as JSON format
    sendData();
    
    lastReading = currentTime;
  }
}

float readVoltage() {
  int sensorValue = analogRead(voltagePin);
  // Convert to actual voltage (adjust based on your voltage divider)
  // For a 25V max with 5:1 divider: multiply by 5
  float voltage = (sensorValue * 5.0 * 5.0) / 1024.0;
  return voltage;
}

float readCurrent() {
  int sensorValue = analogRead(currentPin);
  // Convert to current (adjust based on your current sensor)
  // For ACS712-5A: 185mV/A with 2.5V offset
  float voltage = (sensorValue * 5.0) / 1024.0;
  float current = (voltage - 2.5) / 0.185;
  return abs(current); // Return absolute value
}

void sendData() {
  // Send data in JSON format for easy parsing
  Serial.print("{\"timestamp\":");
  Serial.print(millis());
  Serial.print(",\"voltage\":");
  Serial.print(voltage, 2);
  Serial.print(",\"current\":");
  Serial.print(current, 2);
  Serial.print(",\"temperature\":");
  Serial.print(temperature, 1);
  Serial.print(",\"humidity\":");
  Serial.print(humidity, 1);
  Serial.print(",\"power\":");
  Serial.print(voltage * current, 2);
  Serial.println("}");
}