import pandas as pd
import numpy as np
import folium

# Load sensor data (Assuming you have a CSV file with columns: 'latitude', 'longitude', 'sensor_type', 'value')
data = pd.read_csv('sensor_data.csv')

# Calculate mean and standard deviation for each sensor type
mean_std = data.groupby('sensor_type')['value'].agg(['mean', 'std'])

# Define threshold for anomaly detection (e.g., 2 standard deviations)
threshold = 2

# Detect anomalies based on the defined threshold
data['anomaly'] = np.where(np.abs(data['value'] - mean_std.loc[data['sensor_type'], 'mean']) > threshold * mean_std.loc[data['sensor_type'], 'std'], True, False)

# Initialize folium map centered around Prokhodnaya River
m = folium.Map(location=[54.7318, 56.029], zoom_start=12)

# Add normal data points to the map (blue)
normal_data = data[~data['anomaly']]
for _, row in normal_data.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color='blue').add_to(m)

# Add anomaly data points to the map (red)
anomaly_data = data[data['anomaly']]
for _, row in anomaly_data.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=8, color='red').add_to(m)

# Save the final map
m.save("74.html")