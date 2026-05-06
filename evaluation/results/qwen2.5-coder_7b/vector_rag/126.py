import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на бассейне
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о стоках рек (замените на реальные данные)
shilik_river_flow = {
    "1-3": {"mean": 50, "std_dev": 10},
    "4-6": {"mean": 70, "std_dev": 15},
    "7-9": {"mean": 80, "std_dev": 20},
    "10-12": {"mean": 60, "std_dev": 15}
}

kishi_almaty_river_flow = {
    "1-3": {"mean": 40, "std_dev": 8},
    "4-6": {"mean": 60, "std_dev": 12},
    "7-9": {"mean": 75, "std_dev": 18},
    "10-12": {"mean": 55, "std_dev": 13}
}

# Добавление маркеров на карте для демонстрации данных
for season, data in shilik_river_flow.items():
    folium.Marker(
        location=[centroid.y + 0.1 * (season == '4-6'), centroid.x],
        popup=f"Shilik River - Сезон {season}: Среднее значение - {data['mean']}, Стандартное отклонение - {data['std_dev']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

for season, data in kishi_almaty_river_flow.items():
    folium.Marker(
        location=[centroid.y + 0.1 * (season == '4-6'), centroid.x - 0.2],
        popup=f"Kishi Almaty River - Сезон {season}: Среднее значение - {data['mean']}, Стандартное отклонение - {data['std_dev']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("126.html")