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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
rivers = [
    {"name": "Или", "wkt": "<WKT for Ili River>"},
    {"name": "Сарыкан", "wkt": "<WKT for Sarykan River>"},
    {"name": "Шынжалгы", "wkt": "<WKT for Shynzhaly River>"},
    {"name": "Шыжың", "wkt": "<WKT for Shyzhyn River>"},
    {"name": "Узын Каргалы", "wkt": "<WKT for Uzyn Kargaly River>"}
]

# Add rivers to the map
for river in rivers:
    folium.GeoJson(
        wkt.loads(river["wkt"]),
        style_function=lambda x: {'fillColor': 'blue', 'color': 'blue', 'fillOpacity': 0.5},
        highlight_function=lambda x: folium.GeoJson(
            wkt.loads(river["wkt"]),
            style_function=lambda y: {'fillColor': 'red', 'color': 'red', 'fillOpacity': 0.8},
        ).add_to(m),
    ).add_to(m)

# Save the final map
m.save("156.html")