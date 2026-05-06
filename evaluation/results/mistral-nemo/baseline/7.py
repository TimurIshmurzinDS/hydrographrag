import requests
import folium

# Step 1: Load data from NOAA API
def get_water_level():
    url = 'https://api.noaa.gov/data/2.0/swob/observations?station=8465930&product=water_level&date=latest&DATE=yesterday'
    response = requests.get(url, params={'units': 'metric'})
    data = response.json()
    return data['value']

# Step 2: Create geographical coordinates for Batareyka River
def get_geographical_coordinates():
    latitude = 53.9076
    longitude = 27.4816
    return (latitude, longitude)

# Step 3: Visualize data on map using folium library
def visualize_data_on_map(water_level):
    m = folium.Map(location=get_geographical_coordinates(), zoom_start=15)
    folium.Marker(get_geographical_coordinates(), popup=f'Уровень воды в реке Batareyka River: {water_level} м').add_to(m)
    return m

# Step 4: Save final map as "7.html"
def save_map(map):
    map.save("7.html")

if __name__ == "__main__":
    water_level = get_water_level()
    coordinates = get_geographical_coordinates()
    map = visualize_data_on_map(water_level)
    save_map(map)