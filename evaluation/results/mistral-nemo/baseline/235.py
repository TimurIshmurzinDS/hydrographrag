import folium
import geopandas as gpd
from shapely.geometry import Point

# Шаг 1: Сбор данных о расходе воды реки Или
# Предполагается, что у нас есть данные в формате CSV с полями 'longitude', 'latitude' и 'water_flow'
data = pd.read_csv('ili_river_water_flow.csv')

# Шаг 2: Преобразование данных в формат для моделирования траектории спутника
geometry = [Point(long, lat) for long, lat in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Шаг 3: Моделирование траектории спутника (это может быть сложным процессом, требующим специальных инструментов и библиотек)
# Для этой демонстрации мы просто используем данные о расходе воды для определения начальной точки траектории спутника
initial_point = gdf.iloc[0]['geometry']
m = folium.Map(location=[initial_point.y, initial_point.x], zoom_start=12)

# Шаг 4: Визуализация траектории спутника на карте с использованием библиотеки `folium`
# Для этой демонстрации мы просто добавляем начальный пункт на карту
folium.Marker([initial_point.y, initial_point.x], popup='Initial Point').add_to(m)

# Сохранение карты в файл HTML
m.save("235.html")