import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the dataset
data = pd.read_csv('TATAMOTORS.csv')

# Remove extra spaces from column names
data.columns = data.columns.str.strip()

# Select features and target variable
X = data[['OPEN', 'HIGH', 'LOW', 'PREV. CLOSE']]  # Features: Opening, High, Low, Previous Close
y = data['close']  # Target variable: Closing price

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Predict the stock price for the next year
last_data_point = data.iloc[-1][['OPEN', 'HIGH', 'LOW', 'PREV. CLOSE']].values.reshape(1, -1)
future_price = model.predict(last_data_point)
print("Predicted stock price for the next year:", future_price[0])
