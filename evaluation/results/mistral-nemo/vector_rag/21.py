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

# If coordinates (WKT) are provided, create a hardcoded list of dictionaries
shyzhyn_river_coords = [{'type': 'Point', 'coordinates': [53.1478, 29.6972]}]
shynzhaly_river_coords = [{'type': 'Point', 'coordinates': [53.0956, 29.7453]}]
byzhyi_river_coords = [{'type': 'Point', 'coordinates': [53.1822, 29.5831]}]

# Add rivers to the map
for river in shyzhyn_river_coords + shynzhaly_river_coords + byzhyi_river_coords:
    folium.GeoJson(
        data=river,
        style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.5},
    ).add_to(m)

# Save the final map
m.save("21.html")