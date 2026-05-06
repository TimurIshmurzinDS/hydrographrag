import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Создание карты с центром в бассейне
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты деревень (WKT)
villages_wkt = [
    "POINT(45.123 60.456)",
    "POINT(45.130 60.460)",
    "POINT(45.128 60.458)"
]

# Преобразование WKT в геометрические объекты
villages = gpd.GeoSeries([wkt.loads(w) for w in villages_wkt], crs='EPSG:4326')

# Добавление деревень на карту
for idx, point in enumerate(villages):
    folium.Marker(location=[point.y, point.x], popup=f"Темирлик деревня {idx+1}").add_to(m)

# Сохранение карты в файл
m.save("107.html")