import geopandas as gpd
from folium import Map, Marker
import pandas as pd

# Создать слой с геометрией области интереса (район рек Бутак и Сарыкан)
gdf = gpd.read_file('path_to_your_shapefile.shp')
area_of_interest = gdf[gdf['name'] == 'Река Бутак и Сарыкан']

# Получить список всех датчиков в этой области
sensors_gdf = gpd.read_file('path_to_sensors_shapefile.shp')

# Проверить, передает ли каждый датчик данные без ошибок
def check_sensor_data(sensor):
    # Здесь вы можете добавить свою логику проверки данных датчика
    return True  # или False

sensors_in_area = sensors_gdf[sensors_gdf.intersects(area_of_interest.unary_union)]

# Для каждого датчика в области проверить, передает ли он данные без ошибок
errors_found = False
for index, row in sensors_in_area.iterrows():
    if not check_sensor_data(row):
        print(f'Датчик {row["name"]} не передает данные без ошибок.')
        errors_found = True

# Если есть хотя бы один датчик, который не передает данные без ошибок, вывести сообщение об этом
if errors_found:
    print('Есть датчики, которые не передают данные без ошибок.')

# Создать карту с маркерами для каждого датчика в области
m = Map(location=[45.5236, 122.6750], zoom_start=10)
for index, row in sensors_in_area.iterrows():
    Marker([row['y'], row['x']], popup=row['name']).add_to(m)

# Сохранить карту как HTML-файл
m.save("147.html")