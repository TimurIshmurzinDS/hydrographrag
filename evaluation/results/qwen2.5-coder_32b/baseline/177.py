import geopandas as gpd
from shapely.geometry import LineString, Polygon
import folium

# Загрузка данных (предполагается, что у нас есть GeoJSON файлы с бассейнами рек)
sarikhan_catchment = gpd.read_file('sarikhan_catchment.geojson')
emel_catchment = gpd.read_file('emel_catchment.geojson')

# Функция для вычисления топологической сложности
def calculate_topological_complexity(catchment):
    # Пример простого параметра - количество водотоков (линий)
    num_waterways = len(catchment['waterways'])
    
    # Другие параметры можно добавить, например длина водных сетей
    total_length = catchment['waterways'].length.sum()
    
    # Площадь бассейна
    area = catchment.geometry.area.iloc[0]
    
    return {
        'num_waterways': num_waterways,
        'total_length': total_length,
        'area': area
    }

# Вычисление топологической сложности для каждого бассейна
sarikhan_complexity = calculate_topological_complexity(sarikhan_catchment)
emel_complexity = calculate_topological_complexity(emel_catchment)

print("Топологическая сложность бассейна реки Сарыкан:", sarikhan_complexity)
print("Топологическая сложность бассейна реки Эмель:", emel_complexity)

# Визуализация на карте
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерно по центру бассейнов

# Добавление бассейна реки Сарыкан на карту
folium.GeoJson(sarikhan_catchment, name='Бассейн реки Сарыкан').add_to(m)

# Добавление бассейна реки Эмель на карту
folium.GeoJson(emel_catchment, name='Бассейн реки Эмель', style_function=lambda x: {'color': 'blue'}).add_to(m)

# Добавление легенды
folium.LayerControl().add_to(m)

# Сохранение карты в файл HTML
m.save("177.html")