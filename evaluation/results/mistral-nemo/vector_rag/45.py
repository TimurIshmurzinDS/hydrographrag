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
coordinates = [
    {'type': 'Point', 'coordinates': [longitude, latitude], 'properties': {'Water_consumption_Value': value}},
    # Add more points as needed
]

# Add points to the map using folium.CircleMarker
for coord in coordinates:
    folium.CircleMarker(
        location=coord['coordinates'],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.5,
        popup=f"Water consumption: {coord['properties']['Water_consumption_Value']} m³s",
    ).add_to(m)

# Save the final map
m.save("45.html")