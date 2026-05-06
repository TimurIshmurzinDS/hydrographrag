import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат для верхнего течения реки Тентек и Быж
coordinates = [
    {"name": "Tentek River", "wkt": "POINT(37.123456 55.678901)"},  # Пример WKT координат для верхнего течения Тентек
    {"name": "Byzhy River", "wkt": "POINT(37.123456 55.678901)"}   # Пример WKT координат для верхнего течения Быж
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("94.html")