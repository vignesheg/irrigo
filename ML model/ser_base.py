import pyrebase
import pandas as pd
import joblib
import time
from datetime import datetime, timedelta

# Firebase configuration
firebase_config = {
  'apiKey': "AIzaSyDymuoSQrB855PmttCpUbiOlp6Ag4iraIA",
  'authDomain': "irrigo-dfb76.firebaseapp.com",
  'databaseURL': "https://irrigo-dfb76-default-rtdb.firebaseio.com",
  'projectId': "irrigo-dfb76",
  'storageBucket': "irrigo-dfb76.appspot.com",
  'messagingSenderId': "962205265859",
  'appId': "1:962205265859:web:4bd3bdc9336d24d9c19776",
  'measurementId': "G-743R2SL793"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Load the trained Random Forest model
model_filename = 'rf.joblib'
random_forest_model = joblib.load(model_filename)

# Initialize the last index variable
last_index = ""  # Initialize with -1 to indicate no previous index

def fetch_data_from_firebase():
    # Fetch data from Firebase Realtime Database
    data = db.child("sensors").get().val()
    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)
    df = df.T
    df['soilmoisture']=(df["soilmoisture"]/1023)*100
    return df

def update_status_in_firebase(starttime, endtime, runtime):
    data = {
        "starttime": starttime,
        "endtime": endtime,
        "runtime": runtime
    }
    db.child("statuses").update(data)

def predict_and_update():
    global last_index
    
    # Load the updated dataset from Firebase
    df = fetch_data_from_firebase()
    
    # Ensure the DataFrame is sorted by the index
    df = df.sort_index()
    
    # Get the last row index
    current_index = df.index[-1]
    print(df.tail())
    # Check if the index has changed
    if current_index != last_index:
        # Get the last row (most recent sensor data) and drop the target column
        last_row = df.tail(1)
        
        # Predict motor runtime using the model
        current_prediction = random_forest_model.predict(last_row)[0]
        
        # Print the current prediction
        print(f"Current Prediction: {current_prediction:.2f} Minutes")
        
        # Get the current time as the start time
        starttime = datetime.now().strftime("%H:%M")
        
        # Calculate the end time by adding the predicted runtime to the current time
        endtime = (datetime.now() + timedelta(minutes=current_prediction)).strftime("%H:%M")
        
        # Update the status in Firebase
        update_status_in_firebase(starttime, endtime, current_prediction)
        
        # Update the last index
        last_index = current_index
    else:
        print("No new data yet. Waiting for the next update...")
        print(f"Current update: {current_index}")
        print(f"Last update: {last_index}")
        last_index = current_index

# Main loop to continuously check for updates in the Firebase database
while True:
    predict_and_update()
    
    # Sleep for a short interval before checking again
    time.sleep(10)  # Check every 30 seconds
