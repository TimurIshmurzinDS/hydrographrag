import geopandas as gpd
from shapely.geometry import Polygon
import folium

# Загрузка данных о реках
rivers = gpd.read_file("rivers.shp")

# Определение зоны полива (пример)
irrigation_zone = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])

# Расчет объема воды в реках
volume = rivers.dissolve().geometry.apply(lambda x: x.area * 10) # Пример расчета

# Визуализация на карте
m = folium.Map()
folium.GeoJson("rivers.shp").add_to(m)
folium.GeoJson(irrigation_zone).add_to(m)
m.save("118.html")

print(f"Общий объем воды, доступный для полива: {volume}")