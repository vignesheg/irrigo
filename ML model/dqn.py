import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
import matplotlib.pyplot as plt

# Custom Environment for Irrigation Management
class IrrigationEnv(gym.Env):
    def __init__(self, X, y, linear_model):
        super(IrrigationEnv, self).__init__()

        self.X = X.astype(np.float32)  # Ensure the features are of type float32
        self.y = y.astype(np.float32)  # Ensure the target is of type float32
        self.linear_model = linear_model
        self.current_step = 0

        # Define action space to cover the range of target values, scaled to [-1, 1]
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)

        # Observation space: the features (soil moisture, air humidity, etc.)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(X.shape[1],), dtype=np.float32)

    def reset(self, seed=None, options=None):
        # Handle the seeding requirement
        super().reset(seed=seed)

        self.current_step = 0
        return self.X[self.current_step].astype(np.float32), {}  # Cast to float32 and return observation

    def step(self, action):
        # Rescale the action from [-1, 1] to [0, 1000] (adjust if necessary)
        water_amount = np.clip((action[0] + 1) * 500, 0, 1000)

        # Get the actual water needed from the dataset
        actual_water_needed = self.y[self.current_step]

        # Get the state (observation)
        state = self.X[self.current_step]

        # Predict the water needed using the linear regression model
        linear_pred = self.linear_model.predict(state.reshape(1, -1))[0]

        # Calculate the absolute error
        absolute_error = abs(actual_water_needed - water_amount)

        # Calculate reward based on absolute error (penalize large deviations)
        reward = -absolute_error / actual_water_needed  # Negative reward based on absolute error
        reward = max(reward, -10)  # Penalize large deviations more harshly

        # Reward improvement compared to the linear regression model
        linear_error = abs(actual_water_needed - linear_pred)
        if absolute_error < linear_error:
            reward += 1  # Reward if RL agent's action is better than linear regression

        # Increment step
        self.current_step += 1
        done = self.current_step >= len(self.y)

        # The next state
        if not done:
            next_state = self.X[self.current_step]
        else:
            next_state = np.zeros(self.X.shape[1], dtype=np.float32)  # End of episode

        # Info dictionary to track additional details
        info = {
            'linear_pred': linear_pred,
            'actual_water_needed': actual_water_needed,
            'water_amount': water_amount
        }

        return next_state, reward, done, False, info  # Returning done and truncated as False for Gymnasium

    def render(self, mode='human'):
        pass

file_path = 'random_irrigation_water_needed.csv'
df = pd.read_csv(file_path)

# Prepare the features (X) and target (y)
X = df.drop(columns=['Water_Needed (Liters)']).values
y = df['Water_Needed (Liters)'].values

# Normalize the features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Create the environment using the training data
env = IrrigationEnv(X_train, y_train, linear_model)

# Check the environment (optional but recommended)
check_env(env)

# Wrap the environment with a monitor for training
env = Monitor(env)

# Initialize the PPO agent
model = PPO("MlpPolicy", env, learning_rate=3e-4, verbose=1)

# Train the agent for more iterations
model.learn(total_timesteps=100000)

# Evaluate the agent on the test set
obs, _ = env.reset()
rewards = []
linear_preds = []
actions_taken = []
actual_values = []

for step in range(len(X_test)):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, _, info = env.step(action)
    rewards.append(reward)

    # Log the predictions for comparison
    linear_preds.append(info['linear_pred'])
    actions_taken.append(info['water_amount'])
    actual_values.append(info['actual_water_needed'])

    if done:
        break

print("Total reward:", np.sum(rewards))

# Print comparison of linear regression predictions and agent's actions
comparison_df = pd.DataFrame({
    'Linear Prediction': linear_preds,
    'RL Agent Action': actions_taken,
    'Actual Water Needed': actual_values
})
print(comparison_df.tail(10))  # Print the last 10 comparisons

# Plot key metrics for monitoring the agent's progress
plt.plot(rewards, label='Rewards')
plt.xlabel('Steps')
plt.ylabel('Reward')
plt.title('Reward Progress')
plt.legend()
plt.show()
