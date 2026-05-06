import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Load data for Sharyn and Urjar rivers
sharyn_data = pd.read_csv('sharyn_data.csv')
urjar_data = pd.read_csv('urjar_data.csv')

# Prepare geometry for GeoDataFrame
geometry = [Point(xy) for xy in zip(sharyn_data['longitude'], sharyn_data['latitude'])]
gdf_sharyn = gpd.GeoDataFrame(sharyn_data, geometry=geometry)
gdf_urjar = gpd.GeoDataFrame(urjar_data, geometry=geometry)

# Perform geospatial analysis (e.g., calculate mean values for each river)
mean_sharyn = gdf_sharyn['ecological_status'].mean()
mean_urjar = gdf_urjar['ecological_status'].mean()

# Compare ecological status
if mean_sharyn > mean_urjar:
    comparison_result = 'Экологический статус реки Шарын лучше, чем у реки Уржар.'
elif mean_sharyn < mean_urjar:
    comparison_result = 'Экологический статус реки Уржар лучше, чем у реки Шарын.'
else:
    comparison_result = 'Экологические статусы рек Шарын и Уржар одинаковы.'

print(comparison_result)

# Visualize results on a map using folium
m = folium.Map(location=[sharyn_data['latitude'].mean(), sharyn_data['longitude'].mean()], zoom_start=8)

for _, row in gdf_sharyn.iterrows():
    folium.CircleMarker(location=(row.geometry.y, row.geometry.x), radius=5, color='blue').add_to(m)
for _, row in gdf_urjar.iterrows():
    folium.CircleMarker(location=(row.geometry.y, row.geometry.x), radius=5, color='red').add_to(m)

m.save("188.html")