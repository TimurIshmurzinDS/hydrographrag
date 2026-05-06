import folium
import requests

# Step 1: Load water level data for Kumbel River from the data source
def get_water_level_data():
    # Replace this URL with the actual API or data source URL
    url = "https://example.com/kumbel_river_water_level.json"
    response = requests.get(url)
    return response.json()

# Step 2: Find the latest water level value
def find_latest_water_level(data):
    # Assuming the data is in the format [{'date': 'YYYY-MM-DD', 'level': float}, ...]
    sorted_data = sorted(data, key=lambda x: x['date'], reverse=True)
    return sorted_data[0]['level']

# Step 3: Create a geographical point for Kumbel River location
def create_geographical_point():
    # Replace these coordinates with the actual coordinates of Kumbel River
    lat, lon = 51.5074, -0.1278
    return (lat, lon)

# Step 4: Create a map using folium and add Kumbel River location to it
def create_map(geographical_point):
    m = folium.Map(location=geographical_point)
    folium.Marker(geographical_point).add_to(m)
    return m

# Step 5: Add water level information to the map
def add_water_level_info(map, water_level):
    popup_text = f"Последнее показание уровня воды: {water_level} м"
    folium.CircleMarker(location=create_geographical_point(), radius=10, popup=popup_text).add_to(map)
    return map

# Main function
def main():
    data = get_water_level_data()
    latest_water_level = find_latest_water_level(data)
    geographical_point = create_geographical_point()

    m = create_map(geographical_point)
    m = add_water_level_info(m, latest_water_level)

    # Save the final map as "13.html"
    m.save("13.html")

if __name__ == "__main__":
    main()