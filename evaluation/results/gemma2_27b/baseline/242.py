import geopandas as gpd
from shapely.geometry import Polygon
import folium

# Загрузка данных о реке Тентек
river_data = gpd.read_file("path/to/river_data.shp")

# Выделение разветвления притоков (необходимо доработать)
branches = river_data[river_data["name"] == "Tenek"].explode()

# Создание модели пирога (необходимо доработать)
pie_shape = Polygon(branches.geometry.shapely().exterior)

# Визуализация на карте
m = folium.Map(location=[40, 60], zoom_start=10)
folium.GeoJson(pie_shape).add_to(m)
m.save("242.html")