import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the folium map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name='Basin Boundary'
).add_to(m)

# 4. Handle coordinates from context
# Note: The context provided descriptions but no explicit WKT coordinates.
# If WKT coordinates were provided, they would be added here as a hardcoded list.
observations = [] 

for obs in observations:
    # Example of how points would be added if coordinates existed:
    # folium.Marker([obs['lat'], obs['lon']], popup=obs['name']).add_to(m)
    pass

# 5. Save the final map strictly as "19.html"
m.save("19.html")