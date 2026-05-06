import geopandas as gpd
from shapely.geometry import LineString, Polygon
import folium

# Шаг 1: Подготовка данных
# Предположим, что у нас есть два файла GeoJSON: 'tekes_basin.geojson' и 'drainage_network.geojson'
basin = gpd.read_file('tekes_basin.geojson')
drainage_network = gpd.read_file('drainage_network.geojson')

# Шаг 2: Фильтрация данных
# Выбираем только те участки дренажной сети, которые находятся внутри бассейна реки Текес
drainage_in_basin = gpd.clip(drainage_network, basin)

# Шаг 3: Вычисление общей протяженности дренажных каналов
total_length = drainage_in_basin['geometry'].length.sum()

# Шаг 4: Расчет площади бассейна
basin_area = basin['geometry'].area.sum()

# Шаг 5: Оценка плотности дренажной сети
drainage_density = total_length / basin_area

print(f"Плотность дренажной сети в бассейне реки Текес: {drainage_density} км/км²")

# Шаг 6: Визуализация результатов
# Создаем карту с центром в средней точке бассейна
center = basin['geometry'].centroid.iloc[0]
m = folium.Map(location=[center.y, center.x], zoom_start=10)

# Добавляем границы бассейна на карту
folium.GeoJson(basin).add_to(m)

# Добавляем дренажную сеть на карту
folium.GeoJson(drainage_in_basin, style_function=lambda x: {'color': 'blue'}).add_to(m)

# Добавляем информацию о плотности дренажной сети
folium.Marker(
    location=[center.y, center.x],
    popup=f"Плотность дренажной сети: {drainage_density:.2f} км/км²",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохраняем карту в файл
m.save("172.html")