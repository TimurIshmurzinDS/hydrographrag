import hashlib
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о координатах реки
river = gpd.read_file("path/to/river_data.shp")

# Генерация хэшей для каждой координаты
river["hash"] = river.apply(lambda row: hashlib.sha256(str(row.geometry).encode()).hexdigest(), axis=1)

# Создание карты с Folium
m = folium.Map(location=[river.centroid.y, river.centroid.x], zoom_start=10)

# Добавление координат на карту
for index, row in river.iterrows():
    folium.Marker(location=[row.geometry.y, row.geometry.x], popup=f"Hash: {row['hash']}", tooltip="River Kumbel").add_to(m)

# Сохранение карты
m.save("243.html")