import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_path = r"data/basin_data.shp"
basin_df = gpd.read_file(basin_path)

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the folium map
# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=12, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2,
    name="Basin Boundary"
).add_to(m)

# 4. Handle entities from context
# Note: Context provided entity names but no specific WKT coordinates.
# If WKT coordinates were provided, they would be added here as a list of dictionaries.
entities = [
    {"name": "Terisbuthak Creek", "type": "HY_HydroFeature"},
    {"name": "г. Talgar", "type": "Observation"}
]

# Since no WKT coordinates are present in the provided context, 
# we acknowledge the entities in the map's metadata or as markers if coordinates existed.
# Example of how markers would be added if coordinates were available:
# for entity in entities_with_coords:
#     folium.Marker([entity['lat'], entity['lon']], popup=entity['name']).add_to(m)

# 5. Save the final map strictly as 176.html
m.save("176.html")