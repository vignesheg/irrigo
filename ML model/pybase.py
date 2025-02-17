import pyrebase
import datetime

# Firebase configuration
config = {
  'apiKey': "AIzaSyDymuoSQrB855PmttCpUbiOlp6Ag4iraIA",
  'authDomain': "irrigo-dfb76.firebaseapp.com",
  'databaseURL': "https://irrigo-dfb76-default-rtdb.firebaseio.com",
  'projectId': "irrigo-dfb76",
  'storageBucket': "irrigo-dfb76.appspot.com",
  'messagingSenderId': "962205265859",
  'appId': "1:962205265859:web:4bd3bdc9336d24d9c19776",
  'measurementId': "G-743R2SL793"
}

# Initialize the Firebase app
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Function to add sensor data
def add_sensor_data(air_humidity, soil_moisture, temperature, wind_speed):
    # Get current time as the key
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Data to be added
    data = {
        "Air_Humidity (%)": air_humidity,
        "Soil_Moisture (%)": soil_moisture,
        "Temperature (°C)": temperature,
        "Wind_Speed": wind_speed
    }
    
    # Push data to the 'sensors' node
    db.child("sensors").child(time_now).set(data)
    print(f"Data added for {time_now}")

# Example of adding data
add_sensor_data(86, 29, 24, 2)
