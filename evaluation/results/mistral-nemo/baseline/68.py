import folium
import pandas as pd

# 1. Create a geospatial object for Osek River
river_geojson = {
    'type': 'LineString',
    'coordinates': [(12.345, 56.789), (13.456, 57.890)]
}

# 2. Load sensor data from source
sensor_data = pd.read_csv('sensors.csv')

# 3. Match each sensor with its location on the river map
river_map = folium.Map(location=[river_geojson['coordinates'][0][1], river_geojson['coordinates'][0][0]], zoom_start=12)

folium.GeoJson(river_geojson, style_function=lambda x: {'fillColor': 'blue'}).add_to(river_map)

# 4. Scan sensor status and mark faulty ones on the map
faulty_sensors = []
for _, row in sensor_data.iterrows():
    if row['status'] == 'неисправен':
        folium.Marker([row['latitude'], row['longitude']], popup='Неисправный датчик').add_to(river_map)
        faulty_sensors.append(row)

# 5. Visualize the map with marked faulty sensors
river_map.save("68.html")

# 6. Print faulty sensors data (optional)
print(f"Неисправные датчики:\n{faulty_sensors}")