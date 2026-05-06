import requests
import geopandas as gpd
from shapely.geometry import Point
import folium

# 1. Download river data using API or other sources
url = "https://api.example.com/rivers"
response = requests.get(url)
data = response.json()

# 2. Clean and format the data
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['lon'], data['lat']))

# 3. Find Uzhar and Dos rivers
uzhar_river = gdf[gdf['name'] == 'Уржар']
dos_river = gdf[gdf['name'] == 'Дос']

# 4. Choose hydrological points (e.g., river mouths)
uzhar_point = uzhar_river.iloc[0]['geometry']
dos_point = dos_river.iloc[0]['geometry']

# 5. Calculate distance between the points
distance = uzhar_point.distance(dos_point)

# 6. Visualize rivers on a map using folium
m = folium.Map(location=[uzhar_point.y, uzhar_point.x], zoom_start=12)
folium.GeoJson(uzhar_river[['geometry']]).add_to(m)
folium.GeoJson(dos_river[['geometry']]).add_to(m)

# 7. Save the final map
m.save("96.html")

print(f"Distance between Uzhar and Dos rivers: {distance} meters")