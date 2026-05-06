import folium
import requests

# Replace 'YOUR_API_KEY' with your actual API key for the water level data source
API_KEY = 'YOUR_API_KEY'

# Get current water level data from the API
response = requests.get(f'https://api.example.com/waterlevel?apikey={API_KEY}&river=Prokhodnaya')
data = response.json()
current_water_level = data['water_level']

# Create a map centered on Prokhodnaya River location (latitude, longitude)
m = folium.Map(location=[51.723968, 40.547317], zoom_start=12)

# Add marker for the current water level
folium.Marker([51.723968, 40.547317], popup=f'Текущий уровень воды: {current_water_level} м').add_to(m)

# Save the map as '5.html'
m.save("5.html")