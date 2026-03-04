/*
 * ESP32 Heart Rate Sensor Integration
 * Sends heart rate data to Spring Boot backend
 */

#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Backend server URL
const char* serverUrl = "http://YOUR_SERVER_IP:8080/api/heartrate";

// Heart rate sensor pin (adjust based on your sensor)
const int heartRateSensorPin = A0;

// Timing variables
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 1000; // Send every 1 second

void setup() {
  Serial.begin(115200);
  
  // Initialize WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  // Initialize sensor pin
  pinMode(heartRateSensorPin, INPUT);
}

void loop() {
  unsigned long currentTime = millis();
  
  // Send heart rate data at regular intervals
  if (currentTime - lastSendTime >= sendInterval) {
    float heartRate = readHeartRate();
    
    if (heartRate > 0) {
      sendHeartRateToBackend(heartRate);
    }
    
    lastSendTime = currentTime;
  }
}

/**
 * Read heart rate from sensor
 * Replace this with your actual sensor reading logic
 */
float readHeartRate() {
  // Example: Read from analog pin and convert to BPM
  // This is a placeholder - implement based on your specific sensor
  
  int sensorValue = analogRead(heartRateSensorPin);
  
  // Convert sensor value to BPM (this is sensor-specific)
  // For MAX30102 or similar: use library functions
  // For analog pulse sensor: implement peak detection algorithm
  
  // Placeholder calculation (replace with actual logic)
  float heartRate = map(sensorValue, 0, 4095, 40, 180);
  
  return heartRate;
}

/**
 * Send heart rate data to backend via HTTP POST
 */
void sendHeartRateToBackend(float heartRate) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // Begin HTTP connection
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    // Create JSON payload
    String payload = "{\"heartRate\":" + String(heartRate, 1) + "}";
    
    // Send POST request
    int httpResponseCode = http.POST(payload);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Heart Rate: ");
      Serial.print(heartRate);
      Serial.print(" BPM | Response: ");
      Serial.println(response);
    } else {
      Serial.print("Error sending data: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("WiFi not connected");
  }
}

/* 
 * SENSOR-SPECIFIC IMPLEMENTATIONS
 * Uncomment and use the appropriate section for your sensor
 */

/*
// ===== MAX30102 Pulse Oximeter Sensor =====
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;
float beatsPerMinute;
int beatAvg;

void setupMAX30102() {
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not found");
    while (1);
  }
  
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);
}

float readHeartRateMAX30102() {
  long irValue = particleSensor.getIR();
  
  if (checkForBeat(irValue) == true) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    
    beatsPerMinute = 60 / (delta / 1000.0);
    
    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;
      
      beatAvg = 0;
      for (byte x = 0; x < RATE_SIZE; x++)
        beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
    }
  }
  
  return beatAvg;
}
*/

/*
// ===== Generic Pulse Sensor (Analog) =====
// Uses peak detection algorithm

const int threshold = 550; // Adjust based on your sensor
volatile int BPM;
volatile int Signal;
volatile int IBI = 600;
volatile boolean Pulse = false;
volatile boolean QS = false;

int pulsePin = A0;
int blinkPin = 13;
volatile int rate[10];
volatile unsigned long sampleCounter = 0;
volatile unsigned long lastBeatTime = 0;
volatile int P = 512;
volatile int T = 512;
volatile int thresh = 525;
volatile int amp = 100;
volatile boolean firstBeat = true;
volatile boolean secondBeat = false;

void interruptSetup() {
  // Timer interrupt for sampling at 500Hz (2ms)
  // Implementation depends on your board
}

void getPulse() {
  Signal = analogRead(pulsePin);
  sampleCounter += 2;
  int N = sampleCounter - lastBeatTime;
  
  // Peak detection logic here
  // Update BPM when pulse is detected
  
  // Return average BPM
}
*/
