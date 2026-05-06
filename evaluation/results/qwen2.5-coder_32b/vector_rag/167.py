import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне и преобразование в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты с центроидом бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты наблюдений в формате WKT
observations = [
    {"name": "с.Tekes_1", "geometry": wkt.loads("POINT(86.95 43.05)")},
    {"name": "с.Tekes_2", "geometry": wkt.loads("POINT(87.00 43.10)")},
    {"name": "с.Tekes_3", "geometry": wkt.loads("POINT(86.98 43.08)")}
]

# Добавление наблюдательных пунктов на карту
for obs in observations:
    folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# Предположим, что у нас есть данные о протяженности рек в метрах
length_tekes = 850000  # Примерная протяженность реки Текес в метрах
length_tentek = 120000  # Примерная протяженность реки Тентек в метрах

# Расчет общей протяженности речной сети
total_length = length_tekes + length_tentek

# Вывод результата
print(f"Общая протяженность речной сети, соединяющей реку Текес и реку Тентек: {total_length} м")

# Сохранение карты в файл
m.save("167.html")