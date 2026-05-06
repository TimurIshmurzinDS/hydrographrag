import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне реки
# Используем raw string для пути к файлу, чтобы избежать ошибок интерпретации путей
basin_df = gpd.read_file(r"data/basin_data.shp")

# Приведение к стандартной географической системе координат WGS84
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Инициализация карты
# Вычисляем центроид полигона бассейна для центрирования карты
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=12, 
    tiles='CartoDB positron'
)

# 3. Добавление слоя бассейна на карту
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    tooltip="Basin of Temirlik River"
).add_to(m)

# 4. Добавление точек наблюдения (Observation)
# В контексте указаны объекты Temirlik village, но координаты WKT отсутствуют.
# Если бы координаты были предоставлены, они были бы добавлены здесь в виде списка словарей.
observations = [] 
# Пример структуры, если бы координаты были: 
# observations = [{"name": "Temirlik village Obs 1", "coords": [lat, lon]}]

for obs in observations:
    folium.Marker(
        location=obs["coords"],
        popup=obs["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Сохранение итоговой карты в строго определенный файл
m.save("66.html")