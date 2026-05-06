import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Create a hardcoded list of dictionaries with river coordinates (WKT)
rivers = [
    {'name': 'Karaoy River', 'wkt': 'LINESTRING(-75.123456 39.123456, -75.678901 39.678901)'},
    {'name': 'Baskan River', 'wkt': 'LINESTRING(-76.123456 40.123456, -76.678901 40.678901)'},
    {'name': 'Temirlik River', 'wkt': 'LINESTRING(-77.123456 41.123456, -77.678901 41.678901)'}
]

# Check the current risk of flooding for each river
for river in rivers:
    wkt_river = wkt.loads(river['wkt'])
    folium.GeoJson(
        wkt_river,
        style_function=lambda x: {'fillColor': 'red', 'color': 'darkred', 'fillOpacity': 0.2},
        highlight_function=lambda x: folium.GeoJsonHighlight(style={'fillColor': 'yellow'}),
        tooltip=river['name']
    ).add_to(m)

# Save the final map
m.save("90.html")