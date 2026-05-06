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
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Hardcoded coordinates for Koktal River (WKT)
river_coords = [
    {'type': 'Point', 'coordinates': [43.15, 76.89]}  # Example coordinates for Koktal River
]

# Add river points to the map
for coord in river_coords:
    folium.Marker(wkt.loads(coord['type'] + '(' + ','.join(map(str, coord['coordinates'])) + ')')).add_to(m)

# Save the final map
m.save("4.html")