import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data.__geo_interface__,
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
               highlight_function=lambda x: {'weight': 3}).add_to(m)

# If there are Coordinates (WKT) in the context, create a hardcoded list of dictionaries
water_levels = [
    {"date": "2021-01-01", "level": 5.6, "geometry": wkt.loads("POINT(-73.984 40.7589)")},
    {"date": "2021-02-15", "level": 6.2, "geometry": wkt.loads("POINT(-73.984 40.7589)")}
]

# Add water levels to the map
for level in water_levels:
    folium.CircleMarker(location=[level['geometry'].y, level['geometry'].x], radius=5).add_to(m)

# Save the final map
m.save("272.html")