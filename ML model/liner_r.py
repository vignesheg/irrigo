import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
file_path = 'generated_irrigation_data.csv'
df = pd.read_csv(file_path)

# Prepare the features (X) and target (y)
X = df.drop(columns=['Motor_Runtime (Minutes)'])  # Features
y = df['Motor_Runtime (Minutes)']  # Target

# Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the models
linear_model = LinearRegression()

# Train the Linear Regression model
linear_model.fit(X_train, y_train)
joblib.dump(linear_model, 'lin_rog.joblib')
linear_y_pred = linear_model.predict(X_test)

# Evaluate the models
linear_mse = mean_squared_error(y_test, linear_y_pred)
linear_r2 = r2_score(y_test, linear_y_pred)

print(linear_r2)
