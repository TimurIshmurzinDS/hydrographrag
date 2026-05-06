import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs("EPSG:4326")

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads("POINT (-74.0060 4.5703)"), "properties": {"name": "Karatal River"}},
    {"type": "Feature", "geometry": wkt.loads("POINT (-71.2891 4.6058)"), "properties": {"name": "Koktal River"}},
    {"type": "Feature", "geometry": wkt.loads("POINT (-73.4925 4.7111)"), "properties": {"name": "Bayankol River"}},
    {"type": "Feature", "geometry": wkt.loads("POINT (-70.6845 4.5237)"), "properties": {"name": "Karaoy River"}}
]

# Add the coordinates to the map
for coord in coordinates:
    folium.Marker(
        location=tuple(coord["geometry"].coords[0]),
        popup=coord["properties"]["name"]
    ).add_to(m)

# Save the final map
m.save("214.html")