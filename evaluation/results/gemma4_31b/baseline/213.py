import pandas as pd
import numpy as np
import folium
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta

# =============================================================================
# 1. DATA SIMULATION (Since real Dos River API is not provided)
# =============================================================================
def generate_mock_data():
    # Coordinates for sensors along a hypothetical "Dos River"
    sensors_coords = {
        'Sensor_1': [45.523, -122.676],
        'Sensor_2': [45.530, -122.685],
        'Sensor_3': [45.540, -122.695],
        'Sensor_4': [45.550, -122.710],
        'Sensor_5': [45.560, -122.725]
    }
    
    # Generate time series for 100 hours
    dates = pd.date_range(start="2023-01-01", periods=100, freq='H')
    
    # Sensor readings (e.g., water level in meters)
    sensor_data = {}
    for s in sensors_coords.keys():
        sensor_data[s] = np.random.normal(loc=10, scale=2, size=100)
    
    df_sensors = pd.DataFrame(sensor_data, index=dates)
    
    # Simulate Ethereum Price with some random noise and a slight correlation to Sensor_1
    # Price = Base + (Sensor_1 * factor) + Noise
    eth_price = 1500 + (df_sensors['Sensor_1'] * 15) + np.random.normal(0, 50, 100)
    df_sensors['ETH_Price'] = eth_price
    
    return df_sensors, sensors_coords

# =============================================================================
# 2. MODELING PIPELINE
# =============================================================================
def train_eth_predictor(df):
    # Features: Sensor readings | Target: ETH Price
    X = df.drop(columns=['ETH_Price'])
    y = df['ETH_Price']
    
    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Model: Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict the next value based on the last known sensor readings
    last_reading = X_scaled[-1].reshape(1, -1)
    prediction = model.predict(last_reading)
    
    return prediction[0], model.feature_importances_

# =============================================================================
# 3. GIS VISUALIZATION
# =============================================================================
def create_gis_map(coords, importances, sensor_names):
    # Initialize map centered around the average coordinates
    avg_lat = np.mean([c[0] for c in coords.values()])
    avg_lon = np.mean([c[1] for c in coords.values()])
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=13, tiles='CartoDB dark_matter')
    
    # Map sensors and color them by their importance to the ETH price
    for i, name in enumerate(sensor_names):
        coord = coords[name]
        importance = importances[i]
        
        # Color based on importance (Green = High influence, Red = Low)
        color = 'green' if importance > np.mean(importances) else 'red'
        
        folium.CircleMarker(
            location=coord,
            radius=importance * 100, # Scale radius by importance
            popup=f"{name} | Influence: {importance:.4f}",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)
    
    m.save("213.html")

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    # 1. Get data
    df_data, coords_dict = generate_mock_data()
    sensor_names = list(coords_dict.keys())
    
    # 2. Run prediction model
    predicted_price, feature_importance = train_eth_predictor(df_data)
    
    print(f"--- Ethereum Price Forecast ---")
    print(f"Predicted ETH Price based on Dos River sensors: ${predicted_price:.2f}")
    print(f"-------------------------------")
    
    # 3. Generate GIS map
    create_gis_map(coords_dict, feature_importance, sensor_names)
    print("Map has been saved as 213.html")