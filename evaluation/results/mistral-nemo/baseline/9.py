import requests
import folium
import json

# Replace these URLs with actual APIs or web scraping scripts to get water level data
ili_river_url = "https://api.example.com/ili_river_water_level"
karatal_river_url = "https://api.example.com/karatal_river_water_level"

def get_water_level(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["water_level"]
    else:
        print(f"Error getting water level data: {response.status_code}")
        return None

def visualize_on_map(ili_level, karatal_level):
    m = folium.Map(location=[43.2571, 76.9084], zoom_start=8)  # Start location is somewhere in Kazakhstan

    ili_location = (43.2571, 76.9084)  # Replace with actual coordinates
    karatal_location = (43.2571, 76.9084)  # Replace with actual coordinates

    folium.Marker(ili_location, popup=f"Ili River\nWater Level: {ili_level} m").add_to(m)
    folium.Marker(karatal_location, popup=f"Karatal River\nWater Level: {karatal_level} m").add_to(m)

    m.save("9.html")

if __name__ == "__main__":
    ili_level = get_water_level(ili_river_url)
    karatal_level = get_water_level(karatal_river_url)

    if ili_level and karatal_level:
        visualize_on_map(ili_level, karatal_level)