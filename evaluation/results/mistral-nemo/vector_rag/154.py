import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
shynzhaly_river = {"type": "Feature", "geometry": wkt.loads("POINT(74.56 -18.90)"), "properties": {"Water_level_Value": 25}}
shyzhyn_river = {"type": "Feature", "geometry": wkt.loads("POINT(73.45 -19.23)"), "properties": {"Water_level_Value": 22}}

# Add rivers to the map
folium.GeoJson(shynzhaly_river).add_to(m)
folium.GeoJson(shyzhyn_river).add_to(m)

# Save the final map
m.save("154.html")