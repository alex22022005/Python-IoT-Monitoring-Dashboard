/*
  IoT Monitoring System - Test Data Generator
  Single Arduino UNO sketch for testing Python application
  
  Generates realistic random sensor data:
  - Voltage: 3.0V - 5.2V (simulating power supply variations)
  - Current: 0.1A - 2.5A (simulating load variations)
  - Temperature: 18°C - 35°C (simulating room/ambient temperature)
  
  Data Format: "V:4.85,C:1.23,T:24.5"
  Sends data every 1 second via Serial
*/

// Pin definitions (for reference, not used in simulation)
#define VOLTAGE_PIN A0
#define CURRENT_PIN A1
#define TEMP_PIN A2
#define LED_PIN 13

// Simulation parameters
float baseVoltage = 4.2;      // Base voltage around 4.2V
float baseCurrent = 1.0;      // Base current around 1.0A
float baseTemperature = 22.0; // Base temperature around 22°C

// Trend variables for realistic data
float voltageTrend = 0.0;
float currentTrend = 0.0;
float tempTrend = 0.0;

// Timing
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 1000; // Send data every 1 second

// Data counter
unsigned long dataCount = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  
  // Initialize random seed
  randomSeed(analogRead(A3)); // Use unconnected pin for random seed
  
  // Wait for serial connection
  delay(2000);
  
  // Send startup message
  Serial.println("IoT Monitoring System - Test Data Generator");
  Serial.println("Arduino UNO Ready - Generating Random Sensor Data");
  Serial.println("Data Format: V:voltage,C:current,T:temperature");
  Serial.println("----------------------------------------");
  
  // Blink LED to indicate startup
  for(int i = 0; i < 5; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}

void loop() {
  unsigned long currentTime = millis();
  
  // Send data every second
  if (currentTime - lastSendTime >= sendInterval) {
    // Generate realistic sensor data
    float voltage = generateVoltage();
    float current = generateCurrent();
    float temperature = generateTemperature();
    
    // Send data in the expected format
    sendSensorData(voltage, current, temperature);
    
    // Blink LED to indicate data transmission
    digitalWrite(LED_PIN, HIGH);
    delay(50);
    digitalWrite(LED_PIN, LOW);
    
    lastSendTime = currentTime;
    dataCount++;
    
    // Update trends for more realistic data patterns
    updateTrends();
  }
}

float generateVoltage() {
  // Simulate voltage variations (3.0V to 5.2V)
  // Add some trend and random noise
  float noise = random(-20, 21) / 100.0; // ±0.2V noise
  float trendEffect = sin(millis() / 30000.0) * 0.3; // Slow sine wave trend
  
  float voltage = baseVoltage + voltageTrend + trendEffect + noise;
  
  // Clamp to realistic range
  voltage = constrain(voltage, 3.0, 5.2);
  
  return voltage;
}

float generateCurrent() {
  // Simulate current variations (0.1A to 2.5A)
  // Current often correlates with load changes
  float noise = random(-15, 16) / 100.0; // ±0.15A noise
  float loadVariation = sin(millis() / 20000.0) * 0.4; // Load changes
  
  float current = baseCurrent + currentTrend + loadVariation + noise;
  
  // Clamp to realistic range
  current = constrain(current, 0.1, 2.5);
  
  return current;
}

float generateTemperature() {
  // Simulate temperature variations (18°C to 35°C)
  // Temperature changes slowly and can be affected by current
  float noise = random(-10, 11) / 100.0; // ±0.1°C noise
  float thermalEffect = (baseCurrent - 1.0) * 2.0; // Current affects temperature
  float ambientCycle = sin(millis() / 60000.0) * 3.0; // Slow ambient changes
  
  float temperature = baseTemperature + tempTrend + thermalEffect + ambientCycle + noise;
  
  // Clamp to realistic range
  temperature = constrain(temperature, 18.0, 35.0);
  
  return temperature;
}

void sendSensorData(float voltage, float current, float temperature) {
  // Send data in the format expected by Python application
  Serial.print("V:");
  Serial.print(voltage, 2);
  Serial.print(",C:");
  Serial.print(current, 2);
  Serial.print(",T:");
  Serial.println(temperature, 1);
  
  // Optional: Send debug info every 30 seconds
  if (dataCount % 30 == 0) {
    Serial.print("# Data points sent: ");
    Serial.print(dataCount);
    Serial.print(", Uptime: ");
    Serial.print(millis() / 1000);
    Serial.println(" seconds");
  }
}

void updateTrends() {
  // Update trends every 10 seconds for more realistic long-term patterns
  if (dataCount % 10 == 0) {
    // Voltage trend (slow changes in power supply)
    voltageTrend += random(-5, 6) / 100.0; // ±0.05V change
    voltageTrend = constrain(voltageTrend, -0.3, 0.3);
    
    // Current trend (load changes)
    currentTrend += random(-10, 11) / 100.0; // ±0.1A change
    currentTrend = constrain(currentTrend, -0.5, 0.5);
    
    // Temperature trend (environmental changes)
    tempTrend += random(-5, 6) / 100.0; // ±0.05°C change
    tempTrend = constrain(tempTrend, -2.0, 2.0);
  }
}

// Additional functions for testing different scenarios

void simulateHighLoad() {
  // Simulate high current load scenario
  baseCurrent = 2.0;
  baseTemperature = 28.0;
}

void simulateLowLoad() {
  // Simulate low current load scenario
  baseCurrent = 0.3;
  baseTemperature = 20.0;
}

void simulatePowerFluctuation() {
  // Simulate power supply fluctuations
  baseVoltage = 3.8 + random(-20, 21) / 100.0;
}

// Function to handle serial commands (optional)
void handleSerialCommands() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command == "HIGH_LOAD") {
      simulateHighLoad();
      Serial.println("# Simulating high load scenario");
    }
    else if (command == "LOW_LOAD") {
      simulateLowLoad();
      Serial.println("# Simulating low load scenario");
    }
    else if (command == "POWER_FLUC") {
      simulatePowerFluctuation();
      Serial.println("# Simulating power fluctuations");
    }
    else if (command == "RESET") {
      baseVoltage = 4.2;
      baseCurrent = 1.0;
      baseTemperature = 22.0;
      Serial.println("# Reset to normal parameters");
    }
    else if (command == "STATUS") {
      Serial.print("# Base values - V:");
      Serial.print(baseVoltage);
      Serial.print("V, C:");
      Serial.print(baseCurrent);
      Serial.print("A, T:");
      Serial.print(baseTemperature);
      Serial.println("°C");
    }
  }
}