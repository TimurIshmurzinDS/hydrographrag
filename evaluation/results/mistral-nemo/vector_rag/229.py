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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
# For example:
# river_points = [
#     {'type': 'Feature', 'geometry': wkt.loads('POINT(74.56 -13.90)'), 'properties': {'name': 'Aksu River'}},
#     # Add other points as needed
# ]

# Add river points to the map using folium.CircleMarker
# for point in river_points:
#     folium.CircleMarker(
#         location=tuple(point['geometry'].coords),
#         radius=5,
#         color='red',
#         fill=True,
#         fill_color='red',
#         fill_opacity=0.5,
#     ).add_to(m)

# Save the final map
m.save("229.html")