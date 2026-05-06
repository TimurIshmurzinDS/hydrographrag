import geopandas as gpd
from shapely.geometry import shape, Polygon
import folium

# Загрузка данных о реке Кумбель и агропромышленных объектах
river_data = gpd.read_file('path_to_river_data.shp')
agricultural_complex_data = gpd.read_file('path_to_agricultural_complex_data.shp')

# Определение границы агропромышленного комплекса
complex_boundary = agricultural_complex_data.geometry.unary_union

# Выделение участков реки, попадающих в границы агропромышленного комплекса
river_in_complex = river_data[river_data.geometry.intersects(complex_boundary)]

# Анализ использования воды (пример: суммарное потребление воды)
total_water_consumption = agricultural_complex_data['water_consumption'].sum()

# Визуализация результатов на карте
m = folium.Map(location=[river_in_complex.geometry.centroid.y.mean(), river_in_complex.geometry.centroid.x.mean()], zoom_start=12)

folium.GeoJson(river_in_complex, name='River in Complex').add_to(m)
folium.GeoJson(complex_boundary, style_function=lambda x: {'color': 'red', 'weight': 2}).add_to(m)

folium.LayerControl().add_to(m)

# Сохранение карты
m.save("37.html")

print(f"Общее потребление воды в агропромышленном комплексе: {total_water_consumption}")