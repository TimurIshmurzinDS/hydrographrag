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
    data=r'{"type": "FeatureCollection", "features": [{"type": "Polygon", "coordinates": [[[x0, y0], [x1, y1], ...]]}]}',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
observations = [
    {"type": "Feature", "geometry": wkt.loads('POINT (lon lat)'), "properties": {"name": "Observation_2264"}},
    # Add other observations here...
]

# Add observations to the map
for obs in observations:
    folium.CircleMarker(
        location=tuple(obs['geometry'].coords[0]),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
    ).add_to(m)

# Save the final map
m.save("191.html")