/*
 * ESP32 Breath Rate Sensor Integration
 * Sends breath rate data to backend API
 */

#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Backend server URL
const char* serverUrl = "http://YOUR_SERVER_IP:8080/api/breathrate";

// Breath rate sensor pin (adjust based on your sensor)
const int breathRateSensorPin = A1;

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
  pinMode(breathRateSensorPin, INPUT);
}

void loop() {
  unsigned long currentTime = millis();
  
  // Send breath rate data at regular intervals
  if (currentTime - lastSendTime >= sendInterval) {
    float breathRate = readBreathRate();
    
    if (breathRate > 0) {
      sendBreathRateToBackend(breathRate);
    }
    
    lastSendTime = currentTime;
  }
}

/**
 * Read breath rate from sensor
 * Replace this with your actual sensor reading logic
 */
float readBreathRate() {
  // Example: Read from analog pin and convert to breaths per minute
  // This is a placeholder - implement based on your specific sensor
  
  int sensorValue = analogRead(breathRateSensorPin);
  
  // Convert sensor value to BPM (this is sensor-specific)
  // For respiratory belt sensors: count breaths over time period
  // For optical sensors: detect chest expansion peaks
  
  // Placeholder calculation (replace with actual logic)
  float breathRate = map(sensorValue, 0, 4095, 10, 40);
  
  return breathRate;
}

/**
 * Send breath rate data to backend via HTTP POST
 */
void sendBreathRateToBackend(float breathRate) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // Begin HTTP connection
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    // Create JSON payload
    String payload = "{\"breathRate\":" + String(breathRate, 1) + "}";
    
    // Send POST request
    int httpResponseCode = http.POST(payload);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Breath Rate: ");
      Serial.print(breathRate);
      Serial.print(" BPM | Response: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("WiFi disconnected!");
  }
}
