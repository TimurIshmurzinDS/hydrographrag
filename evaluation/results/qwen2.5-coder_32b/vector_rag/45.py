import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Кумбель из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты предприятий и данные о потреблении воды
# Создание списка словарей с данными о предприятиях
industries = [
    {'name': 'Предприятие_1', 'coordinates': wkt.loads('POINT(37.62 55.75)'), 'consumption_m3s': 0.5, 'date': '2023-01-01'},
    {'name': 'Предприятие_2', 'coordinates': wkt.loads('POINT(37.64 55.76)'), 'consumption_m3s': 0.8, 'date': '2023-01-01'}
]

# Добавление маркеров предприятий на карту
for industry in industries:
    folium.Marker(
        location=[industry['coordinates'].y, industry['coordinates'].x],
        popup=f"{industry['name']}, Потребление: {industry['consumption_m3s']} м³/с, Дата: {industry['date']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("45.html")