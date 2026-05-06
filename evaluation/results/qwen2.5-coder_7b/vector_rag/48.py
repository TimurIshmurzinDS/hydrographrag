import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для информации)
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

# Пример данных о расходе воды (замените на реальные данные)
water_consumption_data = [
    {'date': '2010-01-01', 'value': 500, 'unit': 'm³'},
    {'date': '2010-02-01', 'value': 600, 'unit': 'm³'},
    # Добавьте остальные данные
]

# Пример данных о уровне воды (замените на реальные данные)
water_level_data = [
    {'date': '2010-01-01', 'value': 5.0, 'unit': 'м'},
    {'date': '2010-02-01', 'value': 5.5, 'unit': 'м'},
    # Добавьте остальные данные
]

# Пример данных о расходе воды в Karatal River (замените на реальные данные)
karatal_water_consumption_data = [
    {'date': '2010-01-01', 'value': 300, 'unit': 'm³'},
    {'date': '2010-02-01', 'value': 400, 'unit': 'm³'},
    # Добавьте остальные данные
]

# Пример данных о уровне воды в Karatal River (замените на реальные данные)
karatal_water_level_data = [
    {'date': '2010-01-01', 'value': 4.5, 'unit': 'м'},
    {'date': '2010-02-01', 'value': 5.0, 'unit': 'м'},
    # Добавьте остальные данные
]

# Сохранение карты
m.save("48.html")