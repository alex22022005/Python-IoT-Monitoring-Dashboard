/*
 * Arduino Display Unit with Relays
 * Reads voltage, current, and DHT11 sensors and displays on I2C LCD
 * Controls 2 relays based on sensor readings
 */

#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <Wire.h>

// I2C LCD (address 0x27 for most modules, 16x2 display)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Pin definitions
const int relay1Pin = 4;
const int relay2Pin = 3;
const int voltagePin = A0;   // Analog pin for voltage sensor
const int currentPin = A1;   // Analog pin for current sensor
const int dht11Pin = 7;
const int buzzerPin = 8;
// SDA = A4, SCL = A5 (default I2C pins)

// DHT11 sensor
#define DHT_TYPE DHT11
DHT dht(dht11Pin, DHT_TYPE);

// Variables
float voltage = 0.0;
float current = 0.0;
float temperature = 0.0;
float humidity = 0.0;
bool relay1State = false;
bool relay2State = false;

// Thresholds for relay control
const float voltageThreshold = 12.0;  // Adjust as needed
const float currentThreshold = 2.0;   // Adjust as needed
const float tempThreshold = 30.0;     // Adjust as needed

void setup() {
  // Initialize I2C LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("System Starting...");
  
  // Initialize DHT sensor
  dht.begin();
  
  // Initialize relay pins
  pinMode(relay1Pin, OUTPUT);
  pinMode(relay2Pin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  
  // Set initial relay states (OFF)
  digitalWrite(relay1Pin, LOW);
  digitalWrite(relay2Pin, LOW);
  digitalWrite(buzzerPin, LOW);
  
  delay(2000);
  lcd.clear();
}

void loop() {
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
  
  // Control relays based on sensor readings
  controlRelays();
  
  // Display on LCD
  displayReadings();
  
  delay(2000); // Update every 2 seconds for better readability
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

void displayReadings() {
  static int displayMode = 0;
  static unsigned long lastModeChange = 0;
  unsigned long currentTime = millis();
  
  // Change display mode every 4 seconds
  if (currentTime - lastModeChange >= 4000) {
    displayMode = (displayMode + 1) % 3;
    lastModeChange = currentTime;
    lcd.clear();
  }
  
  switch (displayMode) {
    case 0:
      // Display 1: Voltage and Current
      lcd.setCursor(0, 0);
      lcd.print("V:");
      lcd.print(voltage, 1);
      lcd.print("V  I:");
      lcd.print(current, 2);
      lcd.print("A");
      
      lcd.setCursor(0, 1);
      lcd.print("R1:");
      lcd.print(relay1State ? "ON " : "OFF");
      lcd.print(" R2:");
      lcd.print(relay2State ? "ON " : "OFF");
      break;
      
    case 1:
      // Display 2: Temperature and Humidity
      lcd.setCursor(0, 0);
      lcd.print("Temp: ");
      lcd.print(temperature, 1);
      lcd.print("C");
      
      lcd.setCursor(0, 1);
      lcd.print("Humidity: ");
      lcd.print(humidity, 1);
      lcd.print("%");
      break;
      
    case 2:
      // Display 3: Power and Status
      float power = voltage * current;
      lcd.setCursor(0, 0);
      lcd.print("Power: ");
      lcd.print(power, 1);
      lcd.print("W");
      
      lcd.setCursor(0, 1);
      if (power > 10.0) {
        lcd.print("Status: HIGH");
      } else if (power > 5.0) {
        lcd.print("Status: MED ");
      } else {
        lcd.print("Status: LOW ");
      }
      break;
  }
}

void controlRelays() {
  // Relay 1: Control based on voltage threshold
  if (temperature > 30 && !relay1State) {
    relay1State = true;
    digitalWrite(relay1Pin, HIGH);
    soundBuzzer(1); // Single beep
  } else if (voltage > 35 && relay1State) {
    relay1State = false;
    digitalWrite(relay1Pin, LOW);
  }
  
  // Relay 2: Control based on temperature threshold
  if (temperature > tempThreshold && !relay2State) {
    relay2State = true;
    digitalWrite(relay2Pin, HIGH);
    soundBuzzer(5); // Double beep
  } else if (temperature <= tempThreshold && relay2State) {
    relay2State = false;
    digitalWrite(relay2Pin, LOW);
  }
  
  // Emergency buzzer for high current
  // if (current > currentThreshold) {
  //   soundBuzzer(3); // Triple beep for warning
  // }
}

void soundBuzzer(int beeps) {
  for (int i = 0; i < beeps; i++) {
    digitalWrite(buzzerPin, HIGH);
    delay(100);
    digitalWrite(buzzerPin, LOW);
    if (i < beeps - 1) delay(100);
  }
}