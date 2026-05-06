import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: wkt.dumps(x)).tolist(),
               name='basin',
               style_function=lambda feature: {'color': 'darkgreen', 'weight': 1, 'opacity': 0.2},
               fill_color='green').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {
        'type': 'Feature',
        'geometry': wkt.loads('POINT(47.1234 69.5678)'),
        'properties': {'name': 'Urzhar River'}
    },
    {
        'type': 'Feature',
        'geometry': wkt.loads('POINT(48.9012 68.3456)'),
        'properties': {'name': 'Byzhy River'}
    }
]

# Add the coordinates to the map
folium.Marker([47.1234, 69.5678], popup='Urzhar River').add_to(m)
folium.Marker([48.9012, 68.3456], popup='Byzhy River').add_to(m)

# SAVE the final map: m.save("199.html")
m.save("199.html")