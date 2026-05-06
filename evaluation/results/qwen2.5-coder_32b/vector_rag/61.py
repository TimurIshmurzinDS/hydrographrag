import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Аксу
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты датчиков уровня воды на реке Аксу в формате WKT
sensor_coordinates_wkt = [
    "POINT(76.9184 43.2525)",
    "POINT(76.9200 43.2550)",
    "POINT(76.9250 43.2600)"
]

# Преобразование координат из WKT в точки и добавление на карту
sensors = [wkt.loads(coord) for coord in sensor_coordinates_wkt]
sensor_points = gpd.GeoDataFrame(geometry=sensors, crs='EPSG:4326')

for idx, point in enumerate(sensor_points.geometry):
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Датчик {idx+1}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Сохранение карты в файл
m.save("61.html")