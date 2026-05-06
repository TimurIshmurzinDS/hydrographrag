import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о бассейне из shape-файла и преобразовать их в систему координат EPSG:4326.
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и добавить его на карту.
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_gdf.unary_union.__geo_interface__, name='basin').add_to(m)
m

# Создать список словарей для отображения наблюдений на карте.
observations = [
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.234567, 'lon': 77.890123},
    {'lat': 43.345678, 'lon': 78.901234},
    {'lat': 43.456789, 'lon': 79.012345}
]

# Добавить наблюдения на карту.
for obs in observations:
    folium.Marker(location=[obs['lat'], obs['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл "99.html".
m.save("99.html")