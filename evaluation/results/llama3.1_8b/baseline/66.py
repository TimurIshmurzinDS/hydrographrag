import geopandas as gpd
from folium import Map, Marker

# Шаг 1: Загрузка данных
river_data = gpd.read_file('temirlik_river.shp')
equipment_data = gpd.read_csv('equipment.csv')

# Шаг 2: Создание слоя оборудования
equipment_layer = equipment_data.copy()
equipment_layer['geometry'] = equipment_layer.geometry.apply(lambda x: x.buffer(0.001))  # создаем буфер для точек

# Шаг 3: Слияние слоев реки и оборудования
merged_data = gpd.sjoin(equipment_layer, river_data, how='inner', op='intersects')

# Шаг 4: Фильтрация данных
filtered_data = merged_data[merged_data['equipment_id'] != None]

# Шаг 5: Визуализация результатов
m = Map(location=[45.0, 50.0], zoom_start=10)
for index, row in filtered_data.iterrows():
    Marker([row.geometry.y, row.geometry.x]).add_to(m)

m.save("66.html")