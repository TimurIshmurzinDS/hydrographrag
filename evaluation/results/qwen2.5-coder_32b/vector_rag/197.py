import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат измерений уровня воды (WKT)
coordinates = [
    {"wkt": "POINT(76.9184 43.2525)", "date": "2023-05-01", "water_level": 1200},
    {"wkt": "POINT(76.9184 43.2525)", "date": "2023-05-02", "water_level": 1210},
    # Добавьте больше точек по необходимости
]

# Преобразование координат из WKT в точки и добавление на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=f"Date: {coord['date']}, Water Level: {coord['water_level']} m").add_to(m)

# Сохранение карты в HTML файл
m.save("197.html")