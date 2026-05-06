import geopandas as gpd
import numpy as np
from scipy.spatial import brownian_motion
import folium

# 1. Загрузить данные о речке Шилик в виде вектора линий.
shilka_data = gpd.read_file("shilka.shp")

# 2. Вычислить длину русла реки Шилик.
shilka_length = shilka_data.length.sum()

# 3. Сгенерировать случайные числа на основе модели Брауна с использованием длины реки как параметра.
np.random.seed(0)
random_numbers = brownian_motion(shilka_length, np.random.normal)

# 4. Визуализировать результаты на карте с помощью библиотеки `folium`.
m = folium.Map(location=[shilka_data.y.mean(), shilka_data.x.mean()], zoom_start=10)
folium.GeoJson(
    shilka_data.__geo_interface__,
    style_function=lambda x, y, z: {'fillColor': 'blue', 'color': 'black'},
    highlight_function=lambda x: {'weight': 2},
).add_to(m)

# Сохранить карту как HTML-файл
m.save("254.html")