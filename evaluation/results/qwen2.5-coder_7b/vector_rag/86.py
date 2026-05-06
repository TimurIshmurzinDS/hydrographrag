import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о текущем уровне воды и прогнозах погоды (замените на реальные данные)
water_levels = [
    {'river': 'Karaoy', 'current_level': 150, 'forecasted_level': 160},
    {'river': 'Temirlik', 'current_level': 200, 'forecasted_level': 210},
    {'river': 'Turgen', 'current_level': 180, 'forecasted_level': 190}
]

# Определение опасного роста уровня воды
dangerous_rivers = []
for river in water_levels:
    if river['forecasted_level'] > river['current_level']:
        dangerous_rivers.append(river['river'])

# Добавление маркеров на карту для рек с опасным ростом уровня воды
for river in dangerous_rivers:
    folium.Marker([centroid.y, centroid.x], popup=f"Опасный рост уровня воды на {river}").add_to(m)

# Сохранение карты в файл
m.save("86.html")