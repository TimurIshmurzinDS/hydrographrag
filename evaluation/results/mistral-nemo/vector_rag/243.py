import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[gdf.centroid.y.mean(), gdf.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If coordinates are provided in WKT format, create a hardcoded list of dictionaries
coordinates = [
    {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [long, lat]}},
    # Add more coordinates as needed
]

# Add the coordinates to the map
for coord in coordinates:
    folium.Marker(coord['geometry']['coordinates']).add_to(m)

# Save the final map
m.save("243.html")