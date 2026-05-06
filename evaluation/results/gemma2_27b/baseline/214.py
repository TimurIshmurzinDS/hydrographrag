import geopandas as gpd
import folium

# Загрузка данных о реке Каратал
river = gpd.read_file("karatal_river.shp")

# Буферизация реки
buffer = river.buffer(1000)

# Создание карты
m = folium.Map(location=[42.5, 76], zoom_start=8)

# Добавление буфера на карту
folium.GeoJson(buffer).add_to(m)

# Сохранение карты
m.save("214.html")