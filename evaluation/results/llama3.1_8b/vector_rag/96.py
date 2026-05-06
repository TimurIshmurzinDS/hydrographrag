import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add basin to map
folium.GeoJson(gdf.geometry.__geo_interface__, name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Create hardcoded list of dictionaries for coordinates (WKT)
coords = [
    {
        'type': 'Feature',
        'geometry': wkt.loads('POINT(51.1234 78.5678)'),
        'properties': {'name': 'Устье реки Проходной'}
    },
    {
        'type': 'Feature',
        'geometry': wkt.loads('POINT(51.2345 79.0123)'),
        'properties': {'name': 'Слияние с рекой Оск'}
    }
]

# Add coordinates to map
folium.GeoJson(coords, name='coordinates').add_to(m)

# Save final map
m.save("96.html")