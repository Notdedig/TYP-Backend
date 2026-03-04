/*
 * ESP32 Simple Test - Sends dummy heart rate to backend
 * Use this to test connectivity before adding real sensor
 */

#include <WiFi.h>
#include <HTTPClient.h>

// ===== CONFIGURE THESE =====
const char* ssid = "YOUR_WIFI_SSID";           // Your WiFi name
const char* password = "YOUR_WIFI_PASSWORD";   // Your WiFi password
const char* serverUrl = "http://192.168.1.10:8080/api/heartrate";  // Change to your PC's IP

// Timing
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 1000; // Send every 1 second

// Dummy heart rate (for testing)
float baseHeartRate = 72.0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n=== ESP32 Heart Rate Test ===");
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n✓ WiFi connected!");
  Serial.print("ESP32 IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("Ready to send data to backend...\n");
}

void loop() {
  unsigned long currentTime = millis();
  
  // Send heart rate data every second
  if (currentTime - lastSendTime >= sendInterval) {
    // Generate dummy heart rate (varies between 65-85 BPM)
    float heartRate = baseHeartRate + random(-10, 13);
    
    sendHeartRateToBackend(heartRate);
    
    lastSendTime = currentTime;
  }
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
    
    // Print result
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("✓ Sent HR: ");
      Serial.print(heartRate, 1);
      Serial.print(" BPM | Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("✗ Error code: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("✗ WiFi disconnected!");
  }
}
