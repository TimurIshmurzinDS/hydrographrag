import requests
import folium

# Step 1: Get current water level data from a source (in this example, we'll use a dummy API)
def get_water_level():
    response = requests.get('https://api.example.com/waterlevel/koktal')
    return response.json()['water_level']

# Step 2: Identify the location of Koktal River
koktal_river_location = (49.8503, 67.1524)  # Latitude and longitude of Koktal River

# Step 3: Visualize water depth on a map using Folium
water_level = get_water_level()
m = folium.Map(location=koktal_river_location, zoom_start=12)

folium.Marker(koktal_river_location, popup=f'Глубина воды: {water_level} м').add_to(m)

# Save the final map as "11.html"
m.save("11.html")