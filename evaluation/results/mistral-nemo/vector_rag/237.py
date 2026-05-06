import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
observations = [
    {"type": "Feature", "geometry": wkt.loads('POINT(74.56 39.72)'), "properties": {"Water_consumption_Value": 100, "Water_level_Value": 5}},
    {"type": "Feature", "geometry": wkt.loads('POINT(74.58 39.74)'), "properties": {"Water_consumption_Value": 120, "Water_level_Value": 6}}
]

# Add observations to the map
for obs in observations:
    folium.CircleMarker(location=[obs['geometry'].y, obs['geometry'].x], radius=5).add_to(m)

# Save the final map
m.save("237.html")