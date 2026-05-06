import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
water_levels = [
    {"name": "River1", "coordinates": wkt.loads("POINT(54.987 23.456)", True), "Water_level_Valuecm": 120},
    {"name": "River2", "coordinates": wkt.loads("POINT(-12.345 56.789)", True), "Water_level_Valuecm": 85},
]

# Add water level markers to the map
for level in water_levels:
    folium.Marker(
        location=level["coordinates"],
        popup=f"River: {level['name']}<br>Water Level: {level['Water_level_Valuecm']} cm",
    ).add_to(m)

# Save the final map
m.save("145.html")