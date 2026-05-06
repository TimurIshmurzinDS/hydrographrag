import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (если необходимо)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровне воды (замените на реальные данные)
water_level_data = [
    {'river': 'Bayankol River', 'date': '2013-01-01', 'level': 500},
    {'river': 'Bayankol River', 'date': '2014-01-01', 'level': 510},
    {'river': 'Bayankol River', 'date': '2015-01-01', 'level': 520},
    {'river': 'Kishi Almaty River', 'date': '2013-01-01', 'level': 490},
    {'river': 'Kishi Almaty River', 'date': '2014-01-01', 'level': 500},
    {'river': 'Kishi Almaty River', 'date': '2015-01-01', 'level': 510}
]

# Анализ данных и вычисление волатильности
def calculate_volatility(data):
    levels = [item['level'] for item in data]
    mean_level = sum(levels) / len(levels)
    volatility = max(abs(level - mean_level) for level in levels)
    return volatility

bayankol_volatility = calculate_volatility([item for item in water_level_data if item['river'] == 'Bayankol River'])
kishi_almaty_volatility = calculate_volatility([item for item in water_level_data if item['river'] == 'Kishi Almaty River'])

# Вывод результатов
print(f"Волатильность уровня воды в реке Bayankol River: {bayankol_volatility}")
print(f"Волатильность уровня воды в реке Kishi Almaty River: {kishi_almaty_volatility}")

# Сохранение карты
m.save("134.html")