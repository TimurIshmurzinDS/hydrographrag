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
    {'type': 'Point', 'coordinates': [41.735689, -71.315283]},  # Karkara River location
]

# Add points to the map
for coord in coordinates:
    folium.Marker(wkt.loads(coord['type'] + '(' + ','.join(map(str, coord['coordinates'])) + ')')).add_to(m)

# Save the final map
m.save("54.html")