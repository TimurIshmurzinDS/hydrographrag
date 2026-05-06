import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Прокходная
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты точки наблюдения (пример, так как реальные данные отсутствуют)
observations = [
    {"coordinates": "POINT(37.618423 55.755826)", "value": 10.5},  # Примерные координаты и значение сенсора
    {"coordinates": "POINT(37.618423 55.755826)", "value": 10.4},
    {"coordinates": "POINT(37.618423 55.755826)", "value": 10.6},
    {"coordinates": "POINT(37.618423 55.755826)", "value": 10.3}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs["coordinates"])
    folium.Marker([point.y, point.x], popup=f"Value: {obs['value']}").add_to(m)

# Сохранение карты в файл
m.save("74.html")