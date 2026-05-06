import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Осек из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат наблюдений (WKT) - здесь они не предоставлены, поэтому создаем примерные данные
observations = [
    {"name": "Observation 1", "geometry": wkt.loads("POINT(37.618421 55.755826)")},  # Примерные координаты для наблюдения
    {"name": "Observation 2", "geometry": wkt.loads("POINT(37.619421 55.756826)")},
    {"name": "Observation 3", "geometry": wkt.loads("POINT(37.620421 55.757826)")},
    {"name": "Observation 4", "geometry": wkt.loads("POINT(37.621421 55.758826)" )}
]

# Добавление маркеров наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("238.html")