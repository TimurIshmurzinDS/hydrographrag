import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о потребности в воде (замените на реальные данные)
water_consumption_data = [
    {'date': '2021-01-01', 'value': 500},
    {'date': '2021-02-01', 'value': 600},
    {'date': '2021-03-01', 'value': 550},
    # Добавьте больше данных по необходимости
]

# Вычисление среднего потребления воды
average_water_consumption = sum(item['value'] for item in water_consumption_data) / len(water_consumption_data)

# Площадь бассейна в километрах квадратных
basin_area_km2 = basin_data.iloc[0]['Basin_are_km²']

# Прогнозирование потребности в воде для орошения
estimated_water_consumption = average_water_consumption * basin_area_km2

print(f"Прогнозируемая потребность в воде для орошения: {estimated_water_consumption} м³")

# Сохранение карты
m.save("193.html")