import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты
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
    {'river': 'Koktal River', 'date': '2023-01-01', 'consumption': 500},
    {'river': 'Koktal River', 'date': '2023-07-01', 'consumption': 800},
    {'river': 'Baskan River', 'date': '2023-01-01', 'consumption': 600},
    {'river': 'Baskan River', 'date': '2023-07-01', 'consumption': 900}
]

# Визуализация данных о расходе воды на карте
for data in water_consumption_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Река: {data['river']}, Дата: {data['date']}, Расход: {data['consumption']} м³",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("85.html")