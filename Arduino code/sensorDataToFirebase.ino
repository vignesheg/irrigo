#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <DHT.h>  // Library for DHT11 sensor
#include <OneWire.h>
#include <DallasTemperature.h>


// DS18B20 setup
#define ONE_WIRE_BUS D3        // Pin connected to DS18B20 data pin
OneWire oneWire(ONE_WIRE_BUS); // Setup a oneWire instance to communicate with any OneWire devices
DallasTemperature sensors(&oneWire);  // Pass the oneWire reference to DallasTemperature.0

// Set these to run example.
#define FIREBASE_HOST "irrigo-dfb76-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "cWOx7HSbbwnv7TAvDV766ItqLmzCxGOkSAehz8F3"
#define WIFI_SSID "tracker"
#define WIFI_PASSWORD "123456789"

// NTP setup
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 19800, 60000);

// Software serial for Nano communication
SoftwareSerial nanoSerial(D2, D1); // RX (D2) and TX (D1) pins on ESP8266
String currentTime;
String receivedData;  // Declare receivedData as a global variable

// DHT11 setup
#define DHTPIN D5           // Pin connected to DHT11 data pin
#define DHTTYPE DHT11       // DHT 11 sensor type
DHT dht(DHTPIN, DHTTYPE);

// Soil moisture sensor setup
#define SOIL_MOISTURE_PIN A0 // Analog pin connected to the soil moisture sensor

void setup() {
  Serial.begin(9600); // Serial communication for the NodeMCU monitor
  sensors.begin(); 
  nanoSerial.begin(9600); // Start the software serial at 9600 baud rate to match the Arduino Nano
  
  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());

  // Initialize NTP Client
  timeClient.begin();

  // Initialize Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  // Initialize DHT11 sensor
  dht.begin();
}

void loop() {
  // Update the NTP client for time
  timeClient.update();
  currentTime = timeClient.getFormattedTime();

  // Check for data from the Nano
  if (nanoSerial.available() > 0) {
    receivedData = nanoSerial.readStringUntil('\n'); // Read the incoming data
    Serial.println("Received from Nano: " + receivedData); // Print the received value to serial monitor
  }

  // Request temperature from DS18B20
  sensors.requestTemperatures();
  
  // Get temperature in Celsius
  float temperature = sensors.getTempCByIndex(0);

  // Check if the temperature reading failed
  if (temperature == DEVICE_DISCONNECTED_C) {
    Serial.println("Failed to read from DS18B20 sensor!");
  } else {
    // Print temperature to Serial Monitor
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");
  }

  // Get DHT11 sensor readings
  float humidity = dht.readHumidity();
  
  
  // Get soil moisture sensor value
  int soilMoistureValue = analogRead(SOIL_MOISTURE_PIN);

  // Check if any readings failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print sensor values to Serial
  Serial.println("Current time: " + currentTime);

  
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  
  Serial.print("Soil Moisture: ");
  Serial.println(soilMoistureValue);

  // Send data to Firebase
  Firebase.setFloat("sensors/" + currentTime + "/temperature", temperature);
  Firebase.setFloat("sensors/" + currentTime + "/humidity", humidity);
  Firebase.setFloat("sensors/" + currentTime + "/soilmoisture", soilMoistureValue);
  Firebase.setFloat("sensors/" + currentTime + "/windspeed", rand()%10);

  //current sensor data
    Firebase.setFloat("ctsensors/temperature", temperature);
  Firebase.setFloat("ctsensors/humidity", humidity);
  Firebase.setFloat("ctsensors/soilmoisture", soilMoistureValue);
  Firebase.setFloat("ctsensors/windspeed", rand()%10);
  
  
  // Only send receivedData if it's available (after receiving data from Nano)
 

  delay(5000); // Delay between updates
}