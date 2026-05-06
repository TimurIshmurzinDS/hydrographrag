import folium

# Placeholder for sensor data (replace with actual data)
sensor_data = [
    {"latitude": 40.25, "longitude": 43.15},
    {"latitude": 40.28, "longitude": 43.18},
    {"latitude": 40.30, "longitude": 43.20}
]

# Create a map centered on the Karaoy River
m = folium.Map(location=[40.25, 43.15], zoom_start=12)

# Add sensor locations as markers and connect them with lines
for i in range(len(sensor_data) - 1):
    folium.Marker(location=[sensor_data[i]['latitude'], sensor_data[i]['longitude']]).add_to(m)
    folium.PolyLine([
        [sensor_data[i]['latitude'], sensor_data[i]['longitude']],
        [sensor_data[i+1]['latitude'], sensor_data[i+1]['longitude']]
    ], color="blue").add_to(m)

# Save the map
m.save("216.html")