import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) of river network, create a hardcoded list of dictionaries
river_network = [
    {"name": "Sarykan River", "geometry": wkt.loads("LINESTRING(...)")},
    # Add other rivers here...
]

# Calculate the total length of rivers in the system and the area of Sarykan basin
total_length = sum([wkt.loads(r["geometry"]).length for r in river_network])
basin_area_km2 = gdf['Basin_area_km²'].values[0]

# Calculate the connectivity coefficient K
K = total_length / basin_area_km2

# Save the final map
m.save("175.html")