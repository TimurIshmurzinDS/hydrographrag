import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
# For example:
# river_coords = [
#     {'name': 'Bayankol River', 'wkt': 'POINT(74.56 41.23)'},
#     {'name': 'Shilik River', 'wkt': 'POINT(75.89 40.12)'}
# ]

# For each river, create a point on the map
# for river in river_coords:
#     folium.Marker(location=wkt.loads(river['wkt']), popup=river['name']).add_to(m)

# Save the final map
m.save("121.html")