import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты точек наблюдения в формате WKT
observations_wkt = [
    "POINT(76.9543 42.8123)",  # Примерные координаты для иллюстрации
    "POINT(76.9550 42.8130)",
    "POINT(76.9555 42.8135)"
]

# Преобразование WKT в геометрические объекты
observations = [wkt.loads(obs) for obs in observations_wkt]

# Добавление точек наблюдения на карту
for obs in observations:
    folium.Marker([obs.y, obs.x], popup="Наблюдение").add_to(m)

# Сохранение карты в файл
m.save("95.html")