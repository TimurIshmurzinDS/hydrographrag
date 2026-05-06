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
coordinates = [
    {
        "type": "Feature",
        "geometry": wkt.loads("POINT(74.56 -39.12)"),  # Example coordinate for Aksu River
        "properties": {"name": "AksuRiver", "water_consumption_value": 0.2}
    },
]

# Add the coordinates to the map as markers
for coord in coordinates:
    folium.Marker(
        location=coord["geometry"].coords[0],
        popup=f"{coord['properties']['name']}: {coord['properties']['water_consumption_value']} км³",
    ).add_to(m)

# Save the final map
m.save("33.html")