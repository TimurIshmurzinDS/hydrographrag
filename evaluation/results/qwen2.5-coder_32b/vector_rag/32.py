import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Талгар из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Талгар
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна реки на карту
folium.GeoJson(basin_data.to_json(), name="Бассейн реки Талгар",
               style_function=lambda feature: {
                   'fillColor': 'green',
                   'color': 'darkgreen',
                   'fillOpacity': 0.2,
               }).add_to(m)

# Предположим, что у нас есть координаты точек наблюдений и данные о качестве воды
observations = [
    {'coordinates': wkt.loads('POINT(76.95 43.15)'), 'quality_index': 85},
    {'coordinates': wkt.loads('POINT(77.00 43.20)'), 'quality_index': 78},
    {'coordinates': wkt.loads('POINT(76.98 43.18)'), 'quality_index': 90},
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.CircleMarker(
        location=[obs['coordinates'].y, obs['coordinates'].x],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Качество воды: {obs['quality_index']}",
    ).add_to(m)

# Сохранение карты в файл
m.save("32.html")