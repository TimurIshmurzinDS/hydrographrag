import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize map using the centroid of the shapefile
m = folium.Map(location=gdf.centroid, tiles='CartoDB positron')

# Add basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If coordinates (WKT) are provided in the context, create a hardcoded list of dictionaries
# For example:
# coords = [{'type': 'Point', 'coordinates': [long, lat]}, ...]
# for coord in coords:
#     folium.Marker(location=coord['coordinates']).add_to(m)

# Save the final map
m.save("44.html")