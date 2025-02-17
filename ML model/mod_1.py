import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
file_path = 'random_irrigation_motor_runtime.csv'
df = pd.read_csv(file_path)

# Prepare the features (X) and target (y)
X = df.drop(columns=['Motor_Runtime (Minutes)'])  # Features
y = df['Motor_Runtime (Minutes)']  # Target

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor model
random_forest_model = RandomForestRegressor(random_state=42)

# Train the Random Forest Regressor model
random_forest_model.fit(X_train, y_train)
joblib.dump(random_forest_model, 'rf.joblib')
# Predict on the test data
rf_y_pred = random_forest_model.predict(X_test)

# Evaluate the Random Forest Regressor
rf_mse = mean_squared_error(y_test, rf_y_pred)
rf_r2 = r2_score(y_test, rf_y_pred)

print(f"Random Forest Mean Squared Error: {rf_mse}")
print(f"Random Forest R^2: {rf_r2}")
