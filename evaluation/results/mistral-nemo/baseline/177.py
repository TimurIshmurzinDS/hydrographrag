import folium
import geopandas as gpd
from shapely.geometry import Point

# Шаг 1: Получение данных о реках Сарыкан и Эмель
sarykan_data = {
    'name': 'Сарыкан',
    'geometry': [Point(xy) for xy in [(74.56, 42.89), (74.60, 42.85), ...]],  # Координаты точек вдоль русла реки Сарыкан
    'catchment_area': 12345  # Площадь водосборного бассейна реки Сарыкан в км²
}

emel_data = {
    'name': 'Эмель',
    'geometry': [Point(xy) for xy in [(75.60, 43.21), (75.58, 43.25), ...]],  # Координаты точек вдоль русла реки Эмель
    'catchment_area': 98765  # Площадь водосборного бассейна реки Эмель в км²
}

# Шаг 2: Расчет длины главного стока для каждой реки
def calculate_main_stream_length(geometry):
    return sum([geometry[i].distance(geometry[i+1]) for i in range(len(geometry)-1)])

sarykan_length = calculate_main_stream_length(sarykan_data['geometry'])
emel_length = calculate_main_stream_length(emel_data['geometry'])

# Шаг 3: Расчет индекса топологической сложности для каждого бассейна
def calculate_topological_index(catchment_area, main_stream_length):
    return catchment_area / main_stream_length

sarykan_index = calculate_topological_index(sarykan_data['catchment_area'], sarykan_length)
emel_index = calculate_topological_index(emel_data['catchment_area'], emel_length)

# Шаг 4: Визуализация результатов на карте с использованием библиотеки `folium`
m = folium.Map(location=[43.0, 75.0], zoom_start=8)

sarykan_gdf = gpd.GeoDataFrame({'geometry': sarykan_data['geometry']}, crs='EPSG:4326')
emel_gdf = gpd.GeoDataFrame({'geometry': emel_data['geometry']}, crs='EPSG:4326')

folium.GeoJson(sarykan_gdf, style_function=lambda x: {'fillColor': 'blue'}).add_to(m)
folium.GeoJson(emel_gdf, style_function=lambda x: {'fillColor': 'red'}).add_to(m)

# Добавляем легенду на карту
legend_html = '''
<div style="position: absolute; bottom: 50px; left: 50px; z-index:1000;">
  <div style="background-color: blue; width:20px; height:20px; display:inline-block;"></div>
  Сарыкан<br>
  Индекс топологической сложности: {:.2f}
  <br><br>
  <div style="background-color: red; width:20px; height:20px; display:inline-block;"></div>
  Эмель<br>
  Индекс топологической сложности: {:.2f}
</div>
'''.format(sarykan_index, emel_index)

m.get_root().html.add_child(folium.Element(legend_html))

# Сохраняем карту в файл
m.save("177.html")