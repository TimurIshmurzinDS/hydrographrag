import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование его в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs(epsg=4326)

# Создание карты с центром на centroid бассейна и использованием тайла 'CartoDB positron'
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных уровня воды (WKT)
water_level_data = [
    {'wkt': 'POINT(37.123456 55.678901)', 'date': '2023-10-01', 'level_cm': 120},
    {'wkt': 'POINT(37.123457 55.678902)', 'date': '2023-10-02', 'level_cm': 125}
]

# Добавление точек уровня воды на карту
for data in water_level_data:
    point = wkt.loads(data['wkt'])
    folium.Marker([point.y, point.x], popup=f"Уровень воды: {data['level_cm']} см<br>Дата: {data['date']}", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("13.html")