import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import folium

# Load DEM data (Assuming it's in a GeoTIFF format)
dem = gpd.read_file('path/to/dem.tif')

# Define the points of confluence for rivers Kish-Osek and Talgar
kish_osek_confluence = Point(71.45, 43.25)
talgar_confluence = Point(70.98, 43.67)

# Create a GeoDataFrame with the confluence points
confluences = gpd.GeoDataFrame({
    'geometry': [kish_osek_confluence, talgar_confluence]
})

# Perform flow accumulation using the DEM data to model water flow
flow_accumulation = dem.flowaccumulation()

# Calculate the distance between the two confluence points along the flow path
distance = flow_accumulation.distance(confluences.loc[0, 'geometry'])

# Create a Folium map centered on the average of the two confluence points
m = folium.Map(location=[(kish_osek_confluence.y + talgar_confluence.y) / 2,
                          (kish_osek_confluence.x + talgar_confluence.x) / 2], zoom_start=10)

# Add the DEM data to the map as a heatmap
folium.Choropleth(
    geo_data=dem,
    columns=['Z'],
    key_on='feature.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.8,
    highlight=True
).add_to(m)

# Add the confluence points to the map as markers
for point in confluences.itertuples():
    folium.Marker(location=[point.geometry.y, point.geometry.x]).add_to(m)

# Save the final map
m.save("171.html")