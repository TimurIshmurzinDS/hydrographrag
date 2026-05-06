import geopandas as gpd
import folium

# Загрузить данные о реке Коктал
river = gpd.read_file("path/to/river_data.shp")

# Создать карту Folium
m = folium.Map(location=[river.centroid.y, river.centroid.x], zoom_start=12)

# Добавить слой реки на карту
folium.GeoJson(river).add_to(m)

# Добавить игровые элементы (например, корабль, ресурсы)

# Сохранить карту
m.save("239.html")