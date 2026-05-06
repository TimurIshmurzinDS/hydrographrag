import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты наблюдательных точек в формате WKT
# В реальности эти данные должны быть извлечены из соответствующего источника
observations_wkt = [
    "POINT(37.5 56.0)",
    "POINT(37.51 56.01)",
    "POINT(37.49 55.99)",
    "POINT(37.52 56.02)"
]

# Преобразование WKT в геометрические объекты
observations = [{'geometry': wkt.loads(wkt_str), 'level': None} for wkt_str in observations_wkt]

# Предположим, что уровни воды измерены и сохранены в наблюдениях
# В реальности эти данные должны быть загружены из базы данных или файла
for obs in observations:
    # Здесь мы просто присваиваем случайные значения уровня воды для примера
    obs['level'] = 150 + (obs['geometry'].x - 37.5) * 10 + (obs['geometry'].y - 56.0) * 10

# Определение максимального уровня воды среди наблюдений
max_level_observation = max(observations, key=lambda x: x['level'])

# Добавление всех точек наблюдения на карту
for obs in observations:
    folium.CircleMarker(
        location=[obs['geometry'].y, obs['geometry'].x],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Уровень воды: {obs['level']} см"
    ).add_to(m)

# Добавление точки с максимальным уровнем воды
folium.CircleMarker(
    location=[max_level_observation['geometry'].y, max_level_observation['geometry'].x],
    radius=10,
    color='red',
    fill=True,
    fill_color='red',
    popup=f"Максимальный уровень воды: {max_level_observation['level']} см"
).add_to(m)

# Сохранение карты в файл
m.save("19.html")