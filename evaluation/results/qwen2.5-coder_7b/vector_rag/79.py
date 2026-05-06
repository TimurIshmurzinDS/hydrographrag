import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Turgen River
turgen_river = gpd.read_file(r"data/turgen_river.shp")
turgen_river.crs = 'EPSG:4326'

# Создание карты с центром на реке Turgen River
centroid = turgen_river.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы реки на карту
folium.GeoJson(turgen_river.to_json(), 
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о потреблении воды и уровне воды (замените на реальные данные)
water_consumption_data = [
    {"date": "2023-01-01", "value": 500},
    {"date": "2023-02-01", "value": 600},
    {"date": "2023-03-01", "value": 700},
    {"date": "2023-04-01", "value": 800},
    {"date": "2023-05-01", "value": 900},
    {"date": "2023-06-01", "value": 1000},
    {"date": "2023-07-01", "value": 1100},
    {"date": "2023-08-01", "value": 1200},
    {"date": "2023-09-01", "value": 1300},
    {"date": "2023-10-01", "value": 1400},
    {"date": "2023-11-01", "value": 1500},
    {"date": "2023-12-01", "value": 1600}
]

water_level_data = [
    {"date": "2023-01-01", "value": 10},
    {"date": "2023-02-01", "value": 15},
    {"date": "2023-03-01", "value": 20},
    {"date": "2023-04-01", "value": 25},
    {"date": "2023-05-01", "value": 30},
    {"date": "2023-06-01", "value": 35},
    {"date": "2023-07-01", "value": 40},
    {"date": "2023-08-01", "value": 45},
    {"date": "2023-09-01", "value": 50},
    {"date": "2023-10-01", "value": 55},
    {"date": "2023-11-01", "value": 60},
    {"date": "2023-12-01", "value": 65}
]

# Добавление данных о потреблении воды на карту
for data in water_consumption_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Потребление воды: {data['value']} m³").add_to(m)

# Добавление данных о уровне воды на карту
for data in water_level_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Уровень воды: {data['value']} м").add_to(m)

# Сохранение карты
m.save("79.html")