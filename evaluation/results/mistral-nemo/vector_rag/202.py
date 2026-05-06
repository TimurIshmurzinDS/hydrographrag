import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(basin_data[['geometry']], style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries containing coordinates (WKT) for Emel and Turgen rivers
rivers_coords = [
    {"name": "Emel River", "wkt": "LINESTRING(-75.123456 39.123456, -75.678901 39.678901)"},
    {"name": "Turgen River", "wkt": "LINESTRING(-76.123456 40.123456, -76.678901 40.678901)"}
]

# Create a GeoDataFrame from the list of dictionaries
rivers_gdf = gpd.GeoDataFrame(rivers_coords, geometry=[wkt.loads(coord['wkt']) for coord in rivers_coords])

# Add rivers to the map using folium.GeoJson
folium.GeoJson(rivers_gdf[['geometry']], style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Save the final map
m.save("202.html")