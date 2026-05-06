import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import folium

# Load historical data
data = pd.read_csv('shilik_river_data.csv')

# Select features and target variable
X = data[['temperature', 'precipitation']]
y = data['water_discharge']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f'R² score: {r2}')

# Predict water discharge for next month
next_month_data = pd.DataFrame([[20, 5]], columns=['temperature', 'precipitation'])
predicted_discharge = model.predict(next_month_data)
print(f'Predicted water discharge for next month: {predicted_discharge[0]} cubic meters per second')

# Visualize the location of Shilik River on a map
m = folium.Map(location=[43.2, 76.9], zoom_start=10)

folium.Marker([43.2, 76.9], popup='Shilik River').add_to(m)

m.save("47.html")