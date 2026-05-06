import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2
    }
).add_to(m)

# If there are coordinates for Karaoy River in WKT format, create a list of dictionaries
karaoy_coords = [{'type': 'Point', 'coordinates': (37.5648, 41.9919)}] # Example coordinates for Karaoy River

# Add river points to the map
for coord in karaoy_coords:
    folium.Marker(location=coord['coordinates']).add_to(m)

# Save the final map
m.save("224.html")