import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
n_samples = 30007

# Generate random data for each feature
data = {
    'humidity': np.random.uniform(20, 100, n_samples),  # Air humidity in percentage
    'soilmoisture': np.random.uniform(0, 100, n_samples),  # Soil moisture in percentage
    'temperature': np.random.uniform(-10, 40, n_samples),  # Temperature in Celsius
    'windspeed': np.random.uniform(0, 20, n_samples),  # Wind speed in m/s
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Define the pumping rate of the motor (liters per minute)
pump_rate_liters_per_min = 2  # Example: motor pumps 2 liters per minute

# Define a function to calculate motor runtime in minutes based on other factors
def calculate_motor_runtime(row):
    base_water = 1  # Base water requirement in liters
    water_reduction = row['soilmoisture'] * 0.3  # Water reduction due to soil moisture
    water_increase = (row['temperature'] * 0.5) + (row['windspeed'] * 1)  # Water increase due to temperature and wind speed
    water_needed = base_water - water_reduction + water_increase
    
    # Ensure water needed is within a realistic range
    water_needed = max(0, min(water_needed, 1000))
    
    # Calculate the runtime in minutes
    runtime_minutes = water_needed / pump_rate_liters_per_min
    
    # Adjust runtime into discrete categories
    if runtime_minutes < 0.5:
        return 0
    elif 0.5 <= runtime_minutes <= 1.2:
        return 1
    else:
        return 2
# Apply the function to each row to calculate motor runtime
df['Motor_Runtime (Minutes)'] = df.apply(calculate_motor_runtime, axis=1)

# Display the first few rows of the DataFrame
print(df.tail())
print(df.shape)

# Optionally, save the dataset to a CSV file
df.to_csv('random_irrigation_motor_runtime.csv', index=False)
