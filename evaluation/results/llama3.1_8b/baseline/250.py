import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузите данные о геометрии спутника и топографической сети притоков реки Тентек в формат GeoJSON или Shapefile.
spat_data = gpd.read_file('спутник.geojson')
river_data = gpd.read_file('тентек_притоки.shp')

# Определите координаты центра орбиты спутника
orbital_center = Point(48.8566, 2.3522)  # Координаты Парижа (пример)

# Используйте функцию distance из библиотеки geopandas для расчета расстояния между центром орбиты и каждым элементом топографической сети притоков реки Тентек.
river_data['distance'] = river_data.geometry.distance(orbital_center)

# Если требуется визуализация на карте, используйте библиотеку folium для создания интерактивной карты
m = folium.Map(location=[48.8566, 2.3522], zoom_start=10)
folium.Marker([48.8566, 2.3522], popup='Орбита спутника').add_to(m)

# Добавьте элементы топографической сети притоков реки Тентек на карту
for index, row in river_data.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f'Река {row.name} ({row.distance:.2f} км)').add_to(m)

# Сохраните карту в файл
m.save("250.html")