import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке и городе
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в centroid basin_data
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровне воды (замените на реальные данные)
water_level_value = 150  # Уровень воды в см

# Определение порога уровня воды
threshold = 100  # Порог в см

# Определение состояния реки
if water_level_value > threshold:
    trade_decision = "Покупка криптовалюты"
else:
    trade_decision = "Продажа криптовалюты"

# Добавление информации о торговле на карту
folium.Marker(
    location=[centroid.y, centroid.x],
    popup=f"Уровень воды: {water_level_value} см<br>Решение по торговле: {trade_decision}",
    icon=folium.Icon(color='red' if trade_decision == "Продажа криптовалюты" else 'green')
).add_to(m)

# Сохранение карты
m.save("236.html")