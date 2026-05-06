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

# If context contains Coordinates (WKT), create a hardcoded list of dictionaries
tentek_river = {"type": "Feature", "geometry": wkt.loads("LINESTRING(-75.984 -13.678, -75.982 -13.676)"), "properties": {"name": "Tentek River"}}
temirlik_river = {"type": "Feature", "geometry": wkt.loads("LINESTRING(-75.994 -13.688, -75.992 -13.686)"), "properties": {"name": "Temirlik River"}}

# Add rivers to the map
folium.GeoJson(tentek_river).add_to(m)
folium.GeoJson(temirlik_river).add_to(m)

# Save the final map
m.save("72.html")