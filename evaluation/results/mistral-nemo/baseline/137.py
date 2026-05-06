import folium
import requests

# Load data about monitoring sensors in rivers Ile and Karatal (in GeoJSON format)
sensors_data = requests.get('https://api.example.com/sensors').json()

# Function to check sensor status
def check_sensor_status(sensor_id):
    # Replace with actual API call or database query
    response = requests.get(f'https://api.example.com/sensors/{sensor_id}/status')
    return response.json()['status'] == 'not_working'

# Filter out broken sensors
broken_sensors = [sensor for sensor in sensors_data if check_sensor_status(sensor['id'])]

# Create map with Folium
m = folium.Map(location=[43.2, 76.9], zoom_start=8)

# Add all sensors to the map
for sensor in sensors_data:
    folium.Marker([sensor['latitude'], sensor['longitude']]).add_to(m)

# Highlight broken sensors on the map
for sensor in broken_sensors:
    folium.CircleMarker(
        location=[sensor['latitude'], sensor['longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# Save final map as "137.html"
m.save("137.html")