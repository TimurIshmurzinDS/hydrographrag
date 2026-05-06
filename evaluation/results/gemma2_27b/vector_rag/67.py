import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile and convert to EPSG:4326
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=12)

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of observation points (replace with actual coordinates from data source)
observations = [
    {'location': wkt.loads('POINT (-117.1611 32.7157)'), 'water_level': 2.5},  
    {'location': wkt.loads('POINT (-117.1984 32.7508)'), 'water_level': 3.2}
]

# Add markers for each observation point with water level label
for obs in observations:
    folium.Marker(
        location=[obs['location'].y, obs['location'].x],
        popup=f"Water Level: {obs['water_level']} m",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Save the map
m.save("67.html")