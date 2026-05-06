import geopandas as gpd
from shapely.geometry import Point
from folium import Folium, Marker

# Загружаем данные о реках в формате GeoJSON
shyzyn_data = gpd.read_file('shyzyn.geojson')
dos_data = gpd.read_file('dos.geojson')

# Создаем географическую проекцию для данных
shyzyn_data.crs = 'EPSG:4326'
dos_data.crs = 'EPSG:4326'

# Рассчитываем общую длину речного пути от реки Шыжын до реки Дос, учитывая все промежуточные звенья
total_length = shyzyn_data['length'].sum() + dos_data['length'].sum()

# Создаем карту с помощью библиотеки folium
m = Folium('world')

# Добавляем маркеры на карту для рек Шыжын и Дос
Marker([shyzyn_data.geometry.y, shyzyn_data.geometry.x], popup='Шыжын').add_to(m)
Marker([dos_data.geometry.y, dos_data.geometry.x], popup='Дос').add_to(m)

# Сохраняем карту в формате HTML
m.save("100.html")

print(f'Общая длина речного пути от реки Шыжын до реки Дос составляет {total_length} км.')