import geopandas as gpd
from shapely.geometry import Point
import folium

# Загружаем данные о речной сети в формате вектора
river_network = gpd.read_file("river_network.shp")

# Выделяем ручей Терисбутак как стартовую точку анализа
terisbutak = river_network[river_network['name'] == 'Терисбутак']

# Проанализируем иерархию речной сети с помощью функции "Network Analysis" в QGIS или аналогичного инструмента
# Результаты анализа сохраняем в переменную `analysis_results`

# Визуализируем результаты анализа на карте с использованием библиотеки `folium`
m = folium.Map(location=[terisbutak.geometry.y.mean(), terisbutak.geometry.x.mean()], zoom_start=10)

# Добавляем стартовую точку на карту
folium.Marker([terisbutak.geometry.y, terisbutak.geometry.x], popup='Терисбутак').add_to(m)

# Добавляем результаты анализа на карту
for index, row in analysis_results.iterrows():
    folium.PolyLine(
        [[point.y, point.x] for point in row['geometry'].coords],
        weight=row['weight'],
        color='blue'
    ).add_to(m)

# Сохраняем карту в формате HTML
m.save("170.html")