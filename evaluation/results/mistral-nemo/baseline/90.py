import geopandas as gpd
import pandas as pd
import requests
from folium import FeatureGroup, GeoJson, Map

# Step 1: Create a list of rivers to search
rivers_to_search = ['Karaoy River', 'Baskan River', 'Temirlik River']

# Step 2: Load geodata about rivers from an available source (e.g., OpenStreetMap)
url = "https://geofabrik.de/data/downloads.html?p=asia&l=kg"
response = requests.get(url)
data = response.json()

# Filter data by river names
rivers_data = gpd.read_file(data['features'])
rivers_data = rivers_data[rivers_data['name'].isin(rivers_to_search)]

# Step 3: Calculate current flood risk for each river (using a simple method here)
# Assume we have a 'water_height' column in our data and a threshold for high risk
risk_threshold = 5
rivers_data['flood_risk'] = pd.cut(rivers_data['water_height'], bins=[0, risk_threshold, float('inf')], labels=['Low', 'High'])

# Step 4: Visualize results on a map using folium
m = Map(location=[41.7325, 69.9845], zoom_start=6)

fg_rivers = FeatureGroup("Rivers")
for _, river in rivers_data.iterrows():
    if river['flood_risk'] == 'High':
        color = 'red'
    else:
        color = 'green'
    GeoJson(
        data=[river],
        style_function=lambda x: {'fillColor': color, 'color': 'black', 'weight': 2},
        highlight_function=lambda x: {'fillColor': color, 'color': 'black', 'weight': 3}
    ).add_to(fg_rivers)

fg_rivers.add_to(m)

# Step 6: Save the final map
m.save("90.html")