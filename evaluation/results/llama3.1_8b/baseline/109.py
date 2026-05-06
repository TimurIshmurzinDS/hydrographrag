import geopandas as gpd
from shapely.geometry import shape
import folium

# Загрузим данные о реках и их гидрографических характеристиках.
byzhy_river = gpd.read_file('path/to/byzhy_river.shp')
lepsy_river = gpd.read_file('path/to/lepsy_river.shp')

# Создадим слой данных, представляющий доступность водных ресурсов в каждой реке.
def calculate_water_availability(river):
    river['water_availability'] = river['length'] * river['width']
    return river

byzhy_river = calculate_water_availability(byzhy_river)
lepsy_river = calculate_water_availability(lepsy_river)

# Используем функцию «суммирования» для определения общего объема воды в каждом слое данных.
byzhy_total_water = byzhy_river['water_availability'].sum()
lepsy_total_water = lepsy_river['water_availability'].sum()

print(f'Общий объем воды в реке Byzhy River: {byzhy_total_water} м³')
print(f'Общий объем воды в реке Lepsy River: {lepsy_total_water} м³')

# Сравним объемы воды в двух реках и определим, какая из них более доступна для животноводства.
if byzhy_total_water > lepsy_total_water:
    print('Река Byzhy River более доступна для животноводства.')
elif lepsy_total_water > byzhy_total_water:
    print('Река Lepsy River более доступна для животноводства.')
else:
    print('Обе реки имеют одинаковую доступность для животноводства.')

# Создадим карту с данными о водных ресурсах в каждой реке.
m = folium.Map(location=[55.0, 60.0], zoom_start=10)

folium.Choropleth(
    geo_data='path/to/byzhy_river.shp',
    name='Река Byzhy River',
    data=byzhy_river,
    columns=['water_availability'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

folium.Choropleth(
    geo_data='path/to/lepsy_river.shp',
    name='Река Lepsy River',
    data=lepsy_river,
    columns=['water_availability'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

m.save("109.html")