import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о границах бассейна
# Используем raw-строку для пути к файлу, как того требует инструкция
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Конвертация в стандартную географическую систему координат WGS84
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Инициализация карты
# Вычисляем центроид бассейна для установки начального положения карты
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]

m = folium.Map(
    location=map_center, 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Добавление слоя бассейна на карту
# Применяем строго заданные стили: зеленый цвет заливки и темно-зеленый контур
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name='Basin Boundary'
).add_to(m)

# 4. Добавление постов наблюдения
# В контексте указаны посты, но координаты WKT отсутствуют. 
# Если бы координаты были предоставлены, они были бы добавлены здесь в виде списка словарей.
observations = [] 
# Пример структуры, если бы данные были: 
# observations = [{"name": "2 km above mouth", "coords": [lat, lon], "value": "X.X m"}]

for obs in observations:
    folium.Marker(
        location=obs["coords"],
        popup=f"{obs['name']}: {obs['value']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Сохранение итоговой карты в строго определенный файл
m.save("67.html")