import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs(epsg=4326)

# 3. Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 5. Add the basin boundary to the map
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

# 6. Coordinates for entities (if WKT were provided in context, they would be here)
# Since no specific WKT coordinates were provided in the context, 
# we only visualize the basin boundary.
entities_coords = [] 

for entity in entities_coords:
    folium.Marker(
        location=[entity['lat'], entity['lon']],
        popup=entity['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 7. Save the final map strictly as 33.html
m.save("33.html")