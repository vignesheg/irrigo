import pandas as pd
import numpy as np

# Define ranges and steps
soil_moisture_range = [24, 40, 50, 60, 80]
air_humidity_range = [53, 58, 60, 62, 68]
temperature_range = [34, 32, 31, 29, 27]
water_needed_range = [250, 175, 125, 100, 60]

# Generate 100 rows of random data
np.random.seed(0)
data = {
    'Soil_Moisture (%)': np.random.choice(soil_moisture_range, 10000),
    'Air_Humidity (%)': np.random.choice(air_humidity_range, 10000),
    'Temperature (°C)': np.random.choice(temperature_range, 10000)
}

# Create a DataFrame
df = pd.DataFrame(data)

# Interpolate 'water needed' based on the given data
# We'll use a simple linear interpolation method for this example
def interpolate_water_needed(row):
    sm = row['Soil_Moisture (%)']
    ah = row['Air_Humidity (%)']
    temp = row['Temperature (°C)']
    
    # Simple interpolation based on soil moisture
    if sm <= 40:
        water_needed = 250 - (250 - 175) * (sm - 24) / (40 - 24)
    elif sm <= 50:
        water_needed = 175 - (175 - 125) * (sm - 40) / (50 - 40)
    elif sm <= 60:
        water_needed = 125 - (125 - 100) * (sm - 50) / (60 - 50)
    else:
        water_needed = 100 - (100 - 60) * (sm - 60) / (80 - 60)
    
    return water_needed

df['water_needed (ml)'] = df.apply(interpolate_water_needed, axis=1)

# Save to CSV
df.to_csv('sample_irrigation_data.csv', index=False)
