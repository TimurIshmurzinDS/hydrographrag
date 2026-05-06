import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS for folium compatibility
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
    tooltip="Basin of Dos River"
).add_to(m)

# 4. Handle coordinates for the observation point
# Context mentions: "0.2 km above the confluence with Osek River"
# Since specific WKT coordinates were not provided in the context, 
# we define the logic for adding points if they were present.
observations = [
    # Example structure if WKT were provided:
    # {"name": "Obs Point (0.2km above Osek)", "geometry": wkt.loads("POINT(lon lat)")}
]

for obs in observations:
    folium.Marker(
        location=[obs["geometry"].y, obs["geometry"].x],
        popup=obs["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 56.html
m.save("56.html")