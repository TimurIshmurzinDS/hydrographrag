import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# 1. Загрузить данные о речной сети
river_network = gpd.read_file('rivers.shp')  # Replace with your file path and format

# 2. Отфильтровать речную сеть
teks_and_tentek_rivers = river_network[(river_network['name'] == 'Текес') | (river_network['name'] == 'Тентек')]

# 3. Вычислить общую протяженность отфильтрованной речной сети
total_length = sum(teks_and_tentek_rivers['length'])  # Assuming 'length' is the column containing river lengths

print(f"Общая протяженность речной сети, соединяющей реки Текес и Тентек: {total_length} км")

# 4. Визуализировать результаты на карте
m = folium.Map(location=[teks_and_tentek_rivers['geometry'].centroid.y.mean(), teks_and_tentek_rivers['geometry'].centroid.x.mean()], zoom_start=8)

for _, river in teks_and_tentek_rivers.iterrows():
    folium.GeoJson(river['geometry']).add_to(m)

# Сохранить карту в файл
m.save("167.html")