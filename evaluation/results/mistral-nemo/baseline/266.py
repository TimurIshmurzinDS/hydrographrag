import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import folium

# 1. Подготовьте данные
fields = gpd.read_file("fields.shp") # Замените на путь к вашим данным о полях
terrain = gpd.read_file("terrain.shp") # Замените на путь к вашим данным о местности
river = gpd.read_file("river.shp") # Замените на путь к вашим данным о реке Караой

# 2. Определите зону полива
zone_of_irrigation = gpd.overlay(fields, river, how='intersection')

# 3. Анализ рельефа
dtm = terrain[['geometry', 'elevation']] # Создайте DTM из данных о местности
dtm['x'], dtm['y'] = dtm['geometry'].x, dtm['geometry'].y
slope = np.gradient(dtm['elevation'], axis=0) # Рассчитайте уклон

# 4. Определение путей полива
# (Этот шаг может потребовать дополнительных данных и сложных вычислений,
#  поэтому здесь представлен общий подход, а не конкретный код)

# 5. Визуализация результатов
m = folium.Map(location=[zone_of_irrigation.geometry.y.mean(), zone_of_irrigation.geometry.x.mean()], zoom_start=13)

folium.GeoJson(
    zone_of_irrigation[['geometry']],
    style_function=lambda x, y, z: {'fillColor': 'blue', 'color': 'blue', 'weight': 2},
    highlight_function=lambda x: {'weight': 3}
).add_to(m)

folium.GeoJson(
    terrain[['geometry', 'elevation']],
    style_function=lambda x, y, z: {'fillColor': '#{z}', 'color': '#000', 'weight': 2},
    highlight_function=lambda x: {'weight': 3}
).add_to(m)

m.save("irrigation_model.html")