import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о русле ручья и реке
ru_terisbutak = gpd.read_file("path/to/terisbutak.shp")
river_talgar = gpd.read_file("path/to/talgar.shp")

# Проекция данных (если необходимо)
# ru_terisbutak = ru_terisbutak.to_crs("EPSG:4326") # Пример

# Расчет расстояния
distances = ru_terisbutak.geometry.apply(lambda x: river_talgar.geometry.apply(lambda y: x.distance(y)).min())

ru_terisbutak["distance"] = distances

# Создание карты
m = folium.Map(location=[43.2, 76.9], zoom_start=12)

# Добавление данных на карту
folium.GeoJson("path/to/terisbutak.shp", name="Terisbutak").add_to(m)
folium.GeoJson("path/to/talgar.shp", name="Talgar").add_to(m)

# Визуализация расстояний (потенциально с использованием colormap)
ru_terisbutak["distance"] = ru_terisbutak["distance"].apply(lambda x: round(x, 2))
for index, row in ru_terisbutak.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f"Distance: {row['distance']}").add_to(m)

# Сохранение карты
m.save("176.html")