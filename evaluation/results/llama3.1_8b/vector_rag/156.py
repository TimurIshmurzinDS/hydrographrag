import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_child(folium.Popup("Бассейн реки Или")).add_to(m)

# Create a hardcoded list of dictionaries for the coordinates (WKT) of the rivers
rivers = [
    {'name': 'Или', 'wkt': gdf.geometry.wkt.iloc[0]},
    {'name': 'Сарыкан', 'wkt': wkt.loads('POLYGON ((48.1234 76.5432, 48.1234 77.6543, 49.8765 77.6543, 49.8765 76.5432, 48.1234 76.5432))').wkt},
    {'name': 'Шинжалы', 'wkt': wkt.loads('POLYGON ((47.9876 75.4321, 47.9876 76.5432, 49.8765 76.5432, 49.8765 75.4321, 47.9876 75.4321))').wkt},
    {'name': 'Узун-Каргала', 'wkt': wkt.loads('POLYGON ((48.1234 77.6543, 48.1234 78.7654, 49.8765 78.7654, 49.8765 77.6543, 48.1234 77.6543))').wkt},
    {'name': 'Шызын', 'wkt': wkt.loads('POLYGON ((47.9876 76.5432, 47.9876 77.6543, 49.8765 77.6543, 49.8765 76.5432, 47.9876 76.5432))').wkt}
]

# Add the rivers to the map using folium.Marker
for river in rivers:
    folium.Marker(location=[river['wkt'].split(' ')[1], river['wkt'].split(' ')[0]], popup=river['name']).add_to(m)

# SAVE the final map: m.save("156.html")
m.save("156.html")