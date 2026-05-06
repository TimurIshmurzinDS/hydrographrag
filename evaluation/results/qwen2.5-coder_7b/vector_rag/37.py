import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о потреблении воды и уровне воды (замените на реальные данные)
water_consumption_data = [
    {'date': '2023-01-01', 'consumption': 500, 'level': 10},
    {'date': '2023-01-02', 'consumption': 600, 'level': 12},
    {'date': '2023-01-03', 'consumption': 700, 'level': 15},
    # Добавьте больше данных по необходимости
]

# Визуализация данных о потреблении воды и уровне воды на карте
for data in water_consumption_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Date: {data['date']}, Consumption: {data['consumption']} m³, Level: {data['level']} m",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("37.html")