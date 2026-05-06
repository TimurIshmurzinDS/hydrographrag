import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 (EPSG:4326) for folium compatibility
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Handle coordinates from context
# The context provided entity names but no WKT coordinates.
# If coordinates were provided, they would be added here as a list of dictionaries.
entities_coords = [] 

for entity in entities_coords:
    folium.Marker(
        location=[entity['lat'], entity['lon']],
        popup=entity['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 69.html
m.save("69.html")