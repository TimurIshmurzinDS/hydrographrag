import requests
import folium

# Replace these URLs with actual data sources for river water levels
BASKAN_RIVER_URL = "https://example.com/baskan_river_water_level"
PROKHODNAYA_RIVER_URL = "https://example.com/prokhodnaya_river_water_level"

def get_water_level(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["water_level"]
    else:
        print(f"Error getting water level data: {response.status_code}")
        return None

def is_above_normal(water_level, normal_level):
    return water_level > normal_level

# Normal water levels for Baskan River and Prokhodnaya River during spring thaw
BASKAN_NORMAL_LEVEL = 50
PROKHODNAYA_NORMAL_LEVEL = 45

# Get current water levels
baskan_water_level = get_water_level(BASKAN_RIVER_URL)
prokhodnaya_water_level = get_water_level(PROKHODNAYA_RIVER_URL)

# Check if water levels are above normal
if baskan_water_level is not None:
    is_baskan_above_normal = is_above_normal(baskan_water_level, BASKAN_NORMAL_LEVEL)
else:
    is_baskan_above_normal = False

if prokhodnaya_water_level is not None:
    is_prokhodnaya_above_normal = is_above_normal(prokhodnaya_water_level, PROKHODNAYA_NORMAL_LEVEL)
else:
    is_prokhodnaya_above_normal = False

# Create a map
m = folium.Map(location=[50.6, 37.1], zoom_start=8)

# Add markers for rivers with water levels above normal
if is_baskan_above_normal:
    folium.Marker([49.2, 38.5], popup="Baskan River\nWater level: Above Normal").add_to(m)
if is_prokhodnaya_above_normal:
    folium.Marker([51.0, 36.7], popup="Prokhodnaya River\nWater level: Above Normal").add_to(m)

# Save the map
m.save("81.html")