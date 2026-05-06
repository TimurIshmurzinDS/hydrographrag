import pandas as pd
from sklearn.model_selection import train_test_split
# Choose a model (example: Random Forest)
from sklearn.ensemble import RandomForestRegressor
import folium

# Load historical data
data = pd.read_csv("water_data.csv")

# Preprocess data
features = ["Precipitation", "Runoff", "Evapotranspiration", "Groundwater levels"]
target = "Water availability"
X = data[features]
y = data[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the model (example: Random Forest)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Make predictions for future time points
future_data = pd.read_csv("future_data.csv") # Load data with features for prediction
predictions = model.predict(future_data[features])

# Create a map and visualize the predictions
m = folium.Map(location=[41.38, 72.5], zoom_start=9)

# Add markers to represent predicted water availability
for index, row in future_data.iterrows():
    folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=f"Predicted Water Availability: {predictions[index]}").add_to(m)

m.save("206.html")