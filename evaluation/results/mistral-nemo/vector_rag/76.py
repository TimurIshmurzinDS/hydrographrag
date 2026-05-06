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

# Hardcoded list of dictionaries containing coordinates (WKT) for Karaoy River hydroposts
hydroposts = [
    {'name': 'Hydropost 1', 'geometry': wkt.loads('POINT(45.123 78.901)'), 'risk_level': 'low'},
    {'name': 'Hydropost 2', 'geometry': wkt.loads('POINT(46.234 79.012)'), 'risk_level': 'medium'},
    {'name': 'Hydropost 3', 'geometry': wkt.loads('POINT(47.345 79.123)'), 'risk_level': 'high'}
]

# Add hydroposts to the map with different colors based on risk level
for hp in hydroposts:
    folium.CircleMarker(
        location=hp['geometry'].coords[:],
        radius=8,
        color='green' if hp['risk_level'] == 'low' else ('yellow' if hp['risk_level'] == 'medium' else 'red'),
        fill=True,
        fill_color='green' if hp['risk_level'] == 'low' else ('yellow' if hp['risk_level'] == 'medium' else 'red')
    ).add_to(m)

# Save the final map
m.save("76.html")