import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If we have coordinates (WKT) for Ili River, create a hardcoded list of dictionaries
ili_river_coords = [{'type': 'Feature', 'geometry': wkt.loads('POINT(74.56 -81.34)')}]
for coord in ili_river_coords:
    folium.Marker(coord['geometry']).add_to(m)

# Save the final map
m.save("31.html")