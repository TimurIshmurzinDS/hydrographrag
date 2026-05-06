import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование CRS
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты folium с центром в центроиде бассейна
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты точек в формате WKT (примерные данные)
points_wkt = [
    {"name": "Point_1", "wkt": "POINT(48.35 57.65)"},  # Примерная точка на расстоянии 2 км выше устья Прокходного ручья
    {"name": "Point_2", "wkt": "POINT(48.36 57.66)"}   # Примерная точка на расстоянии 0.2 км выше слияния с Осекой
]

# Преобразование WKT в геометрические объекты и добавление их на карту
for point in points_wkt:
    geom = wkt.loads(point["wkt"])
    folium.Marker([geom.y, geom.x], popup=point["name"]).add_to(m)

# Сохранение карты в файл
m.save("96.html")