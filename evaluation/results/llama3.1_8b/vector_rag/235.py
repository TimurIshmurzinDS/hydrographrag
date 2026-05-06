import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
centroid = gdf.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for the observation points
observation_points = [
    {'location': [46.1234, 69.5678], 'popup': 'Пункт наблюдения в 0,2 км выше устья реки Оск'},
    {'location': [46.2345, 70.0123], 'popup': 'Пункт наблюдения в 0,2 км выше устья реки Оск'},
    {'location': [46.3456, 70.4578], 'popup': 'Пункт наблюдения в 0,2 км выше устья реки Оск'}
]

# Add observation points to the map
for point in observation_points:
    folium.Marker(point['location'], popup=point['popup']).add_to(m)

# Save the final map strictly using a string filename
m.save("235.html")