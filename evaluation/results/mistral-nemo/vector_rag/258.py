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
emel_river = {
    'type': 'Feature',
    'geometry': wkt.loads('LINESTRING(....)'),  # Replace with actual WKT coordinate string for Emel River
    'properties': {'name': 'Emel River'}
}
kumbel_river = {
    'type': 'Feature',
    'geometry': wkt.loads('LINESTRING(....)'),  # Replace with actual WKT coordinate string for Kumbel River
    'properties': {'name': 'Kumbel River'}
}
bayankol_river = {
    'type': 'Feature',
    'geometry': wkt.loads('LINESTRING(....)'),  # Replace with actual WKT coordinate string for Bayankol River
    'properties': {'name': 'Bayankol River'}
}

# Add rivers to the map
for river in [emel_river, kumbel_river, bayankol_river]:
    folium.GeoJson(
        data=river,
        style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.5},
    ).add_to(m)

# Save the final map
m.save("258.html")