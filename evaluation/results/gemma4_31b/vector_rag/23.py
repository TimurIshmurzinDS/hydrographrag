import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map with specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    tooltip='Basin Boundary'
).add_to(m)

# Context contains observation points but no WKT coordinates were provided.
# If WKT coordinates were present, they would be added here as a list of dictionaries.
observations = [] 

# Add observation points to the map if they exist
for obs in observations:
    folium.Marker(
        location=[obs['lat'], obs['lon']],
        popup=obs['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Save the final map strictly as 23.html
m.save("23.html")