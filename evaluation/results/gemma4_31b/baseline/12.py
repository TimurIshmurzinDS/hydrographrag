import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

# 1. Simulation of Sensor Data
def generate_sensor_data():
    np.random.seed(42)
    # Coordinates for sensors along the hypothetical Prokhodnaya River
    sensors_info = {
        'S1': {'lat': 55.75, 'lon': 37.61, 'status': 'Normal'},
        'S2': {'lat': 55.76, 'lon': 37.63, 'status': 'Outliers'},
        'S3': {'lat': 55.77, 'lon': 37.65, 'status': 'Flatline'},
        'S4': {'lat': 55.78, 'lon': 37.67, 'status': 'Missing'},
    }
    
    data_list = []
    time_range = pd.date_range(start="2023-10-01", periods=100, freq='H')
    
    for s_id, info in sensors_info.items():
        base_value = 2.5 + np.random.random()
        values = base_value + np.random.normal(0, 0.1, size=100)
        
        # Injecting errors
        if info['status'] == 'Outliers':
            values[20:25] = values[20:25] * 10  # Sudden spike
        elif info['status'] == 'Flatline':
            values[40:] = values[40]  # Sensor freezes
        elif info['status'] == 'Missing':
            values[10:30] = np.nan  # Data gap
            
        for t, v in zip(time_range, values):
            data_list.append({'sensor_id': s_id, 'timestamp': t, 'value': v, 'lat': info['lat'], 'lon': info['lon']})
            
    return pd.DataFrame(data_list), sensors_info

# 2. Error Detection Logic
def analyze_sensors(df):
    results = {}
    sensors = df['sensor_id'].unique()
    
    for s_id in sensors:
        s_data = df[df['sensor_id'] == s_id]['value']
        errors = []
        
        # Check for Missing Values
        if s_data.isna().sum() > 5:
            errors.append("Missing Data")
            
        # Check for Flatline (Zero variance)
        if s_data.std() == 0 or (s_data.dropna().std() == 0):
            errors.append("Flatline/Frozen")
            
        # Check for Outliers using Z-score
        mean = s_data.mean()
        std = s_data.std()
        if std > 0:
            z_scores = np.abs((s_data - mean) / std)
            if z_scores.max() > 3:
                errors.append("Outliers Detected")
        
        results[s_id] = errors if errors else ["OK"]
        
    return results

# 3. Main Execution
def main():
    # Generate data
    df, sensors_meta = generate_sensor_data()
    
    # Analyze data
    health_report = analyze_sensors(df)
    
    # Create Folium Map
    # Centered around the hypothetical river area
    m = folium.Map(location=[55.76, 37.64], zoom_start=12, tiles='OpenStreetMap')
    
    # Add a polyline to simulate the river
    river_coords = [[55.75, 37.61], [55.76, 37.63], [55.77, 37.65], [55.78, 37.67]]
    folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.7, tooltip="Prokhodnaya River").add_to(m)
    
    # Add sensor markers
    for s_id, info in sensors_meta.items():
        status = health_report[s_id]
        color = 'green' if status == ["OK"] else 'red'
        status_text = ", ".join(status)
        
        folium.CircleMarker(
            location=[info['lat'], info['lon']],
            radius=8,
            popup=f"Sensor: {s_id}<br>Status: {status_text}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)
    
    # Save map
    m.save("12.html")
    print("Analysis complete. Map saved as 12.html")
    print("\nSensor Health Report:")
    for s, res in health_report.items():
        print(f"Sensor {s}: {res}")

if __name__ == "__main__":
    main()