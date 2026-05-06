import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs(epsg=4326)

# Calculate the centroid of the basin to initialize the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map
m = folium.Map(location=map_center, zoom_start=8, tiles='CartoDB positron')

# Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    name='Basin Boundary'
).add_to(m)

# The context provided mentions an observation point 0.2 km above the confluence with Osek River,
# but no specific WKT coordinates were provided in the context for Dos or Emel rivers.
# If coordinates were present, they would be added here as a list of dictionaries.
points_of_interest = []

# Add points to map if they exist
for point in points_of_interest:
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=point['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Save the final map strictly as 92.html
m.save("92.html")