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
water_level_data = [
    {'geometry': wkt.loads('POINT(74.56 -51.23)', srs='EPSG:4326'), 'Water_level_Valuecm': 100},
    {'geometry': wkt.loads('POINT(74.57 -51.24)', srs='EPSG:4326'), 'Water_level_Valuecm': 120},
]

# Add water level data to the map
for data in water_level_data:
    folium.CircleMarker(
        location=data['geometry'].coords[:],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.5,
    ).add_to(m)

# Save the final map
m.save("264.html")