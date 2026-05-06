import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с внешними границами бассейна
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(gdf.to_json(), name='bassien').add_to(m)

# Создание списка словарей для координат ручья Терисбутак (hardcoded)
terisbuthak_coords = [
    {'lat': 55.1234, 'lon': 36.7890},
    {'lat': 55.1245, 'lon': 36.7901},
    {'lat': 55.1256, 'lon': 36.7912}
]

# Добавление координат ручья Терисбутак на карту
folium.Marker([55.1234, 36.7890], popup='Ручей Терисбутак').add_to(m)

# Сохранение карты в файл с именем "170.html"
m.save("170.html")