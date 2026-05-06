import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о реках
rivers = gpd.read_file("rivers.shp") # Заменить "rivers.shp" на путь к файлу с данными о реках

# Определение истока реки Тентек
tentek = rivers[rivers["name"] == "Тентек"].iloc[0].geometry
source_tentek = tentek.interpolate(0)

# Получение координат устья реки Быж
byzh = rivers[rivers["name"] == "Быж"].iloc[0]
mouth_byzh = byzh.geometry.interpolate(1)

# Сравнение координат
print("Координаты истока Тентек:", source_tentek.x, source_tentek.y)
print("Координаты устья Быж:", mouth_byzh.x, mouth_byzh.y)

# Визуализация на карте
m = folium.Map(location=[45.0, 80.0], zoom_start=7) # Заменить координаты центра карты

folium.Marker(location=[source_tentek.y, source_tentek.x], popup="Источник Тентек").add_to(m)
folium.Marker(location=[mouth_byzh.y, mouth_byzh.x], popup="Устье Быж").add_to(m)

m.save("94.html")