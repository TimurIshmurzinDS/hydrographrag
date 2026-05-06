import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_path = r"data/basin_data.shp"
basin_df = gpd.read_file(basin_path)

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# 4. Handle coordinates from context
# The context provided entity names but no specific WKT coordinates.
# If WKT coordinates were provided, they would be added here as a hardcoded list.
entities_coords = [] 

# Example of how coordinates would be added if they existed in context:
# entities_coords = [
#     {"name": "Tentek River", "geometry": wkt.loads("LINESTRING(...)")},
#     {"name": "Tekes River", "geometry": wkt.loads("LINESTRING(...)")},
#     {"name": "с.Tekes", "geometry": wkt.loads("POINT(...)")}
# ]

# Adding entities to map if coordinates were available
for entity in entities_coords:
    geom = entity["geometry"]
    if geom.geom_type == 'Point':
        folium.Marker([geom.y, geom.x], popup=entity["name"]).add_to(m)
    elif geom.geom_type == 'LineString':
        coords = [[p[1], p[0]] for p in geom.coords]
        folium.PolyLine(coords, popup=entity["name"], color='blue').add_to(m)

# 5. Save the final map strictly as 167.html
m.save("167.html")