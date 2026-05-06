import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Или из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна реки Или на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты точки наблюдения для расхода воды (примерные координаты)
observation_points = [
    {"name": "Наблюдение 1", "coordinates": wkt.loads("POINT(76.85 43.90)")}
]

# Добавление точек наблюдения на карту
for point in observation_points:
    folium.Marker(
        location=[point['coordinates'].y, point['coordinates'].x],
        popup=point["name"],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("235.html")