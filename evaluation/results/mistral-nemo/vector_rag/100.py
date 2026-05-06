import geopandas as gpd
import folium
from shapely import wkt

# Hardcoded list of dictionaries containing coordinates in WKT format for each river
rivers = [
    {'name': 'Shyzhyn River', 'wkt': 'LINESTRING(-50.123 40.456, -50.789 40.234)'},
    {'name': 'Byzhy River', 'wkt': 'LINESTRING(-51.234 41.567, -51.890 41.345)'},
    {'name': 'Shynzhaly River', 'wkt': 'LINESTRING(-52.345 42.678, -52.901 42.432)'},
    {'name': 'Prokhodnaya River', 'wkt': 'LINESTRING(-53.456 43.789, -53.901 43.543)'}
]

# Load shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin.centroid.xy), tiles='CartoDB positron')

# Add basin to the map
folium.GeoJson(
    basin,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Calculate total length of river path
total_length = 0

for i in range(len(rivers) - 1):
    line1 = wkt.loads(rivers[i]['wkt'])
    line2 = wkt.loads(rivers[i + 1]['wkt'])

    if not line1.intersects(line2):
        raise ValueError(f"Rivers {rivers[i]['name']} and {rivers[i + 1]['name']} do not intersect.")

    intersection = line1.intersection(line2).length
    total_length += intersection

# Save the final map
m.save("100.html")