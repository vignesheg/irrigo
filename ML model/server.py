import pandas as pd
import joblib
import time

# Load the trained Random Forest model
model_filename = 'rf.joblib'
random_forest_model = joblib.load(model_filename)

# Initialize the last index variable
last_index = -1  # Initialize with -1 to indicate no previous index

def predict_and_print():
    global last_index
    
    # Load the updated dataset
    file_path = 'random_irrigation_motor_runtime.csv'
    df = pd.read_csv(file_path)
    
    # Get the last row index
    current_index = df.index[-1]
    
    # Check if the index has increased by 1
    if current_index == last_index + 1:
        # Get the last row (most recent sensor data) and drop the target column
        last_row = df.tail(1).drop(columns=['Motor_Runtime (Minutes)'])
        
        # Predict motor runtime using the model
        current_prediction = random_forest_model.predict(last_row)[0]
        
        # Print the current prediction
        print(f"Current Prediction: {current_prediction:.2f} Minutes")
        
        # Update the last index
        last_index = current_index
    else:
        print("No new data yet. Waiting for the next update...")
        print(f"Current index: {current_index}")
        print(f"Last index: {last_index}")
        last_index = current_index
# Main loop to continuously check for updates in the dataset
while True:
    predict_and_print()
    
    # Sleep for a short interval before checking again
    time.sleep(10)  # Check every 10 seconds
