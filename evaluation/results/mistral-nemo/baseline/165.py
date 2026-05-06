import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Load data
river_data = pd.read_csv('river_data.csv')
weather_data = pd.read_csv('weather_data.csv')

# Prepare geometry for GeoPandas
geometry = [Point(xy) for xy in zip(river_data['longitude'], river_data['latitude'])]
gdf = gpd.GeoDataFrame(river_data, geometry=geometry)

# Perform geospatial analysis (e.g., calculate distance between rivers)
shyzhyn_river = gdf[gdf['river_name'] == 'Shyzhyn River']
sarykan_river = gdf[gdf['river_name'] == 'Sarykan River']

# Calculate distance between rivers
distance = shyzhyn_river.distance(sarykan_river)

# Perform flood modeling (example: using height data)
height_data = river_data.groupby('river_name')['water_height'].mean()
flood_risk = pd.DataFrame({'river_name': ['Shyzhyn River', 'Sarykan River'], 'flood_risk': [height_data['Shyzhyn River'], height_data['Sarykan River']]})

# Visualize results on map using folium
m = folium.Map(location=[shyzhyn_river.geometry.y.mean(), shyzhyn_river.geometry.x.mean()], zoom_start=10)

for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

# Save the map as HTML file
m.save("165.html")