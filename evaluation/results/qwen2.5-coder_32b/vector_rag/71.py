import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Создание карты с центроидом бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты сенсоров в формате WKT и их состояния
sensors = [
    {"wkt": "POINT(51.3456 72.8901)", "status": "active"},
    {"wkt": "POINT(51.3567 72.9012)", "status": "inactive"},
    {"wkt": "POINT(51.3678 72.9123)", "status": "active"}
]

# Добавление сенсоров на карту
for sensor in sensors:
    point = wkt.loads(sensor["wkt"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Status: {sensor['status']}",
        icon=folium.Icon(color='green' if sensor['status'] == 'active' else 'red')
    ).add_to(m)

# Сохранение карты
m.save("71.html")