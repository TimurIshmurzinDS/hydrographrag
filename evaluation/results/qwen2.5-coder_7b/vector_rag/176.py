import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для контекста)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты ручья Терисбутак и города Talgar (пример)
terisbuthak_coords = "POINT(45.123456 78.901234)"  # Пример WKT координат
talgar_coords = "POINT(45.567890 79.123456)"    # Пример WKT координат

# Создание геометрий из WKT
terisbuthak_geom = wkt.loads(terisbuthak_coords)
talgar_geom = wkt.loads(talgar_coords)

# Добавление точек на карту
folium.Marker([terisbuthak_geom.y, terisbuthak_geom.x], popup='Ручье Терисбутак', icon=folium.Icon(color='red')).add_to(m)
folium.Marker([talgar_geom.y, talgar_geom.x], popup='Город Talgar', icon=folium.Icon(color='blue')).add_to(m)

# Рассчет расстояния между точками
distance = terisbuthak_geom.distance(talgar_geom).item()
print(f"Расстояние от ручья Терисбутак до города Talgar: {distance} м")

# Сохранение карты
m.save("176.html")