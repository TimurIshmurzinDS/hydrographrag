import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for the path as per critical instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map
# Using 'CartoDB positron' tiles as required
m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

# 5. Add the basin boundary to the map
# Strict styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 6. Handle Coordinates/Observations
# Context mentions an observation point 1.7 km above the mouth of Kishi Osek River.
# Since specific WKT coordinates were not provided in the context string, 
# we ensure the logic for hardcoded lists is present if coordinates were available.
# Example structure for future WKT additions:
# observations = [
#     {"name": "Obs Point Kishi Osek", "geometry": wkt.loads("POINT(lon lat)")}
# ]
# for obs in observations:
#     folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# 7. Save the final map strictly as "206.html"
m.save("206.html")