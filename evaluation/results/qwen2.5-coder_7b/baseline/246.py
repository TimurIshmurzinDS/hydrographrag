import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных созвездия Ориона (пример координат)
orion_constellation = [
    (10.6847, 35.9222),  # Betelgeuse
    (10.6847, 35.9222),  # Alnitak
    (10.6847, 35.9222),  # Mintaka
    (10.6847, 35.9222)   # Saiph
]

# Загрузка данных реки Шилик (пример координат)
shiliq_river = [
    (10.6847, 35.9222),  # Начало реки
    (10.6847, 35.9222),  # Конец реки
]

# Создание GeoDataFrame для созвездия Ориона
orion_gdf = gpd.GeoDataFrame(geometry=[Point(coord) for coord in orion_constellation])

# Создание GeoDataFrame для реки Шилик
shiliq_gdf = gpd.GeoDataFrame(geometry=[LineString(coord) for coord in shiliq_river])

# Визуализация данных на карте
m = folium.Map(location=[35.9222, 10.6847], zoom_start=10)

for idx, row in orion_gdf.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=f"Betelgeuse {idx}").add_to(m)

folium.PolyLine(shiliq_river[0][0], shiliq_river[0][1], color='blue').add_to(m)

# Сохранение карты
m.save("246.html")