import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах рек
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в среднем значении координат бассейнов
centroid = basin_data.geometry.centroid.unary_union.centroid
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейнов рек на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о датчиках уровня воды (заменить на реальные данные)
sensor_data = [
    {'coordinates': wkt.loads('POINT(37.6173 55.7558)'), 'water_level_cm': 150, 'classification': 'нормальный'},
    {'coordinates': wkt.loads('POINT(37.6273 55.7458)'), 'water_level_cm': 200, 'classification': 'предупреждение'},
    {'coordinates': wkt.loads('POINT(37.6373 55.7358)'), 'water_level_cm': 250, 'classification': 'опасность'}
]

# Добавление маркеров на карту
for data in sensor_data:
    folium.Marker(
        location=[data['coordinates'].y, data['coordinates'].x],
        popup=f"Уровень воды: {data['water_level_cm']} см\nСостояние: {data['classification']}",
        icon=folium.Icon(color='green' if data['classification'] == 'нормальный' else ('orange' if data['classification'] == 'предупреждение' else 'red'))
    ).add_to(m)

# Сохранение карты
m.save("145.html")