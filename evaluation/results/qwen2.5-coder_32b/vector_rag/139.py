import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне Сарыкан
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о датчиках уровня воды (WKT координаты и значения)
sensor_data = [
    {"coordinates": "POINT(76.95 43.15)", "water_level_cm": 150, "date": "2023-10-01"},
    {"coordinates": "POINT(77.00 43.20)", "water_level_cm": 200, "date": "2023-10-01"},
    {"coordinates": "POINT(76.98 43.18)", "water_level_cm": 50, "date": "2023-10-01"}
]

# Определение нормального диапазона уровня воды (примерные значения)
normal_range = (100, 180)  # в сантиметрах

# Добавление маркеров на карту
for sensor in sensor_data:
    point = wkt.loads(sensor["coordinates"])
    if not normal_range[0] <= sensor["water_level_cm"] <= normal_range[1]:
        folium.Marker(
            location=[point.y, point.x],
            popup=f"Аномальный уровень воды: {sensor['water_level_cm']} см\nДата: {sensor['date']}",
            icon=folium.Icon(color='red')
        ).add_to(m)

# Сохранение карты
m.save("139.html")