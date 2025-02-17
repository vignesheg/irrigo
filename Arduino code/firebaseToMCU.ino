#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define FIREBASE_HOST "irrigo-dfb76-default-rtdb.firebaseio.com"  // Firebase URL
#define FIREBASE_AUTH "cWOx7HSbbwnv7TAvDV766ItqLmzCxGOkSAehz8F3"  // Firebase Database Secret
#define WIFI_SSID "tracker"
#define WIFI_PASSWORD "123456789"
int relayPin = D5;  // Define the pin connected to the relay
#define WATER_LEVEL_PIN A0  // Define the analog pin for the water level sensor

// Variables for start and end times
String startTime;
String endTime;
String currentTime;
int waterLevelThreshold = 500;  // Set a threshold f.or the water level (adjust based on the sensor)

// NTP Client setup
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 19800, 60000);  // IST offset is 19800 seconds (5.5 hours)

void setup() {
  Serial.begin(115200);
  
    pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);  // Initialize relay state
  pinMode(WATER_LEVEL_PIN, INPUT);  // Initialize water level sensor

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize NTP client
  timeClient.begin();

  // Initialize Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop() {
  int mode = Firebase.getInt("statuses/mode");
  int mtstatus = Firebase.getInt("statuses/mtstatus");

  if (Firebase.failed()) {
    Serial.print("Firebase failed: ");
    Serial.println(Firebase.error());
    return;
  }

  // Read the water level from the sensor
  int waterLevel = analogRead(WATER_LEVEL_PIN);
  Serial.print("Water Level: ");
  Serial.println(waterLevel);

  // Upload water level data to Firebase
  Firebase.setInt("statuses/waterLevel", waterLevel);

  if (Firebase.failed()) {
    Serial.print("Failed to send water level to Firebase: ");
    Serial.println(Firebase.error());
  }

  if (mode == 1 && mtstatus == 1) {
    // Retrieve start and end times from Firebase
    startTime = Firebase.getString("statuses/manstarttime");  
    endTime = Firebase.getString("statuses/manendtime");      

    if (Firebase.failed()) {
      Serial.print("Firebase get failed: ");
      Serial.println(Firebase.error());
      return;
    }

    Serial.println("Start Time: " + startTime);
    Serial.println("End Time: " + endTime);

    timeClient.update();
    currentTime = timeClient.getFormattedTime().substring(0, 5);  
    Firebase.setString("statuses/servertime");
    Serial.println("Current Time (IST): " + currentTime);

    if (currentTime >= startTime && currentTime < endTime) {
      Serial.println("Relay ON (Water level sufficient)");
       digitalWrite(relayPin, LOW); // Active Low relay
    } else {
      Serial.println("Relay OFF (Time out or water level low)");
      digitalWrite(relayPin, HIGH); // Active Low relay
    }
  } else if (mode == 2 && mtstatus == 1) {
    // Retrieve auto start and end times from Firebase
    startTime = Firebase.getString("statuses/starttime");  
    endTime = Firebase.getString("statuses/endtime");      

    if (Firebase.failed()) {
      
      Serial.print("Firebase get failed: ");
      Serial.println(Firebase.error());
      return;
    }

    Serial.println("Auto Start Time: " + startTime);
    Serial.println("Auto End Time: " + endTime);

    timeClient.update();
    currentTime = timeClient.getFormattedTime().substring(0, 5);  
    Serial.println("Current Time (IST): " + currentTime);

    if (currentTime >= startTime && currentTime < endTime) {
      Serial.println("Relay ON (Water level sufficient)");
      digitalWrite(relayPin, LOW);  // Active Low relay
    } else {
      Serial.println("Relay OFF (Time out or water level low)");
      digitalWrite(relayPin, HIGH); // Active Low relay
    }
  }

  if(mtstatus != 1){
    digitalWrite(relayPin, HIGH); // Active Low relay
  }

  delay(5000);  // Check every 10 seconds
}
