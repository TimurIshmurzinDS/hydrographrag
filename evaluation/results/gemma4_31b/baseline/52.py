import pandas as pd
import numpy as np
import folium
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, rmse_score # Note: using mean_squared_error for RMSE
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 1. Synthetic Data Generation (Simulating Sarykan River Hydrology)
# In a real scenario, this would be replaced by a CSV or API call to a hydro-station
np.random.seed(42)
dates = pd.date_range(start="2015-01-01", end="2023-12-31", freq='M')
n = len(dates)

# Simulate precipitation (higher in spring/autumn)
precip = 20 + 15 * np.sin(2 * np.pi * np.arange(n) / 12) + np.random.normal(0, 5, n)
# Simulate temperature (seasonal cycle)
temp = 10 + 20 * np.sin(2 * np.pi * np.arange(n) / 12 - np.pi/2) + np.random.normal(0, 3, n)
# Simulate flow (depends on precip, temp and lag)
flow = np.zeros(n)
for i in range(1, n):
    # Flow is a function of current precip, temp (snowmelt) and previous flow
    flow[i] = 0.5 * flow[i-1] + 0.8 * precip[i] + 0.4 * max(0, temp[i]) + np.random.normal(0, 2)

df = pd.DataFrame({'date': dates, 'precip': precip, 'temp': temp, 'flow': flow})

# 2. Feature Engineering
def create_features(data):
    df_feat = data.copy()
    df_feat['month'] = df_feat['date'].dt.month
    df_feat['flow_lag1'] = df_feat['flow'].shift(1)
    df_feat['flow_lag3'] = df_feat['flow'].shift(3)
    df_feat['precip_lag1'] = df_feat['precip'].shift(1)
    return df_feat.dropna()

df_model = create_features(df)

# 3. Model Training
X = df_model[['precip', 'temp', 'month', 'flow_lag1', 'flow_lag3', 'precip_lag1']]
y = df_model['flow']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validation
preds = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, preds))
print(f"Model Validation RMSE: {rmse:.2f}")

# 4. Forecasting for the Next Season (6 months)
last_data = df_model.iloc[-1:]
future_dates = pd.date_range(start="2024-01-01", periods=6, freq='M')
forecasts = []

# Simple recursive forecast
current_flow = last_data['flow'].values[0]
current_precip = last_data['precip'].values[0]

for i in range(6):
    # Assume average seasonal precip and temp for the next season
    f_precip = 20 + 15 * np.sin(2 * np.pi * (n + i) / 12)
    f_temp = 10 + 20 * np.sin(2 * np.pi * (n + i) / 12 - np.pi/2)
    f_month = future_dates[i].month
    
    # Using simplified lag for forecast
    feat = np.array([[f_precip, f_temp, f_month, current_flow, current_flow, f_precip]])
    pred_flow = model.predict(feat)[0]
    forecasts.append(pred_flow)
    current_flow = pred_flow
    current_precip = f_precip

print("Forecasted flow for next 6 months:", np.round(forecasts, 2))

# 5. Geospatial Visualization
# Approximate coordinates for Sarykan River region (Central Asia/Kazakhstan area)
river_coords = [46.5, 62.0] 

m = folium.Map(location=river_coords, zoom_start=7, tiles='OpenStreetMap')

# Simulate river basin points
points = [
    {"loc": [46.6, 62.1], "name": "Station Alpha (Upper)", "status": "Normal"},
    {"loc": [46.4, 62.3], "name": "Station Beta (Middle)", "status": "Warning"},
    {"loc": [46.2, 62.5], "name": "Station Gamma (Lower)", "status": "Normal"},
]

for p in points:
    color = 'red' if p['status'] == 'Warning' else 'blue'
    folium.CircleMarker(
        location=p['loc'],
        radius=8,
        popup=f"{p['name']} - Status: {p['status']}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Add a polyline to represent the river
folium.PolyLine(
    locations=[p['loc'] for p in points],
    color="blue",
    weight=4,
    opacity=0.8,
    tooltip="Sarykan River Course"
).add_to(m)

# Save the map
m.save("52.html")
print("Map has been saved as 52.html")