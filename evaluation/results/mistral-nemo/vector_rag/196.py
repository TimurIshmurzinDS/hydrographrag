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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
koksu_river = {"type": "Feature", "geometry": wkt.loads("LINESTRING(...)"),
              "properties": {"name": "Koksu River"}}
emel_river = {"type": "Feature", "geometry": wkt.loads("LINESTRING(...)"),
             "properties": {"name": "Emel River"}}

# Add rivers to the map
for river in [koksu_river, emel_river]:
    folium.GeoJson(river).add_to(m)

# Save the final map
m.save("196.html")