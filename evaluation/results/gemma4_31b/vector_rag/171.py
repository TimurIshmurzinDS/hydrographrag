import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_df,
    name="Basin Boundary",
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# The context provided mentions an observation point 0.2 km above the confluence,
# but no specific WKT coordinates were provided in the input text.
# If coordinates were present, they would be added here as a list of dictionaries.
points_to_plot = []

for point in points_to_plot:
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=point['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Save the final map strictly as 171.html
m.save("171.html")