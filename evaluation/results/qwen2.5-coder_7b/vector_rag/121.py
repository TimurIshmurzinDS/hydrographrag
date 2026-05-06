import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile и заданием тайлов
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о расходе воды в реках (замените на реальные данные)
water_flow_data = [
    {'name': 'Bayankol River', 'flow_rate': 150, 'year': 2023},
    {'name': 'Shilik River', 'flow_rate': 120, 'year': 2023},
    # Добавьте данные за последние 9 лет для каждой из рек
]

# Вычисление среднего расхода воды для каждой речи
bayankol_avg_flow = sum(flow['flow_rate'] for flow in water_flow_data if flow['name'] == 'Bayankol River') / len(water_flow_data)
shilik_avg_flow = sum(flow['flow_rate'] for flow in water_flow_data if flow['name'] == 'Shilik River') / len(water_flow_data)

# Добавление меток на карте с средним расходом воды
folium.Marker([centroid.y, centroid.x], popup=f"Средний расход воды в Bayankol River: {bayankol_avg_flow} м³/с", icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([centroid.y + 0.1, centroid.x], popup=f"Средний расход воды в Shilik River: {shilik_avg_flow} м³/с", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("121.html")