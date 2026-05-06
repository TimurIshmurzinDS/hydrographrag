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

# Hardcoded list of dictionaries containing coordinates (WKT)
coordinates = [
    {'type': 'Point', 'coordinates': [51.5074, -0.1278], 'properties': {'Water_level_Value': 123, 'Date_water_level_Value': '2022-01-01', 'Water_level_Valuecm': 123}},
    {'type': 'Point', 'coordinates': [51.5094, -0.1378], 'properties': {'Water_level_Value': 125, 'Date_water_level_Value': '2022-02-15', 'Water_level_Valuecm': 125}},
    {'type': 'Point', 'coordinates': [51.5114, -0.1478], 'properties': {'Water_level_Value': 126, 'Date_water_level_Value': '2022-03-10', 'Water_level_Valuecm': 126}}
]

# Add points to the map
for coord in coordinates:
    folium.Marker(location=coord['coordinates'], popup=f"Уровень воды: {coord['properties']['Water_level_Value']} м\nДата измерения: {coord['properties']['Date_water_level_Value']}\nУровень воды в сантиметрах: {coord['properties']['Water_level_Valuecm']} см").add_to(m)

# Save the final map
m.save("13.html")