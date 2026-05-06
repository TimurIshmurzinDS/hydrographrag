import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
import folium

# Step 1: Get the data for Baskan River and spacecraft orbit
baskan_river = gpd.read_file('baskan_river.shp')
spacecraft_orbit = [(lat, lon) for lat, lon in zip([...], [])]  # Replace [...] with actual spacecraft orbit coordinates

# Step 2: Get elevation data for Baskan River and spacecraft orbit
elevation_baskan = pd.read_csv('elevation_baskan.csv')  # Replace with actual elevation data file
elevation_spacecraft = pd.read_csv('elevation_spacecraft.csv')  # Replace with actual elevation data file

# Step 3: Check if the spacecraft can reach Baskan River
def can_reach_baskan(river, orbit):
    for lat, lon in orbit:
        point = Point(lon, lat)
        if any(LineString([point, river.geometry[i]]).length < 1000 for i in range(len(river))):  # Assuming spacecraft can reach up to 1 km away from the river
            return True
    return False

# Step 4: Visualize the results on a map
m = folium.Map(location=[...], zoom_start=...)  # Replace [...] with actual coordinates and zoom level

# Add Baskan River to the map
for i in range(len(baskan_river)):
    folium.GeoJson(
        baskan_river.iloc[i]['geometry'],
        style_function=lambda x, y: {'fillColor': 'blue', 'color': 'black'},
        highlight_function=lambda x: {'weight': 2},
    ).add_to(m)

# Add spacecraft orbit to the map
for lat, lon in spacecraft_orbit:
    folium.CircleMarker(location=[lat, lon], radius=5, color='red').add_to(m)

if can_reach_baskan(baskan_river, spacecraft_orbit):
    folium.PolyLine(spacecraft_orbit, weight=3, color='green').add_to(m)
else:
    folium.PolyLine(spacecraft_orbit, weight=3, color='red').add_to(m)

m.save("259.html")