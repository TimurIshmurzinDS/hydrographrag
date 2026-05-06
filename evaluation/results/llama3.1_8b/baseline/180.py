import geopandas as gpd
from shapely.geometry import shape
import folium

# Загрузим данные о реках Текес и Сарыкан в виде геометрических объектов (геометрии)
gdf_tekes = gpd.read_file('tekesshapes.shp')
gdf_sarykan = gpd.read_file('sarykanshapes.shp')

# Создадим сетку для моделирования речной сети
from descartes import PolygonPatch
import matplotlib.pyplot as plt

def create_network(gdf_tekes, gdf_sarykan):
    # Сетка для моделирования речной сети
    x_min, y_min = gdf_tekes.total_bounds[0], gdf_tekes.total_bounds[1]
    x_max, y_max = gdf_sarykan.total_bounds[2], gdf_sarykan.total_bounds[3]

    # Размер области
    width = 10000
    height = 10000

    # Шаг сетки
    dx = dy = 500

    # Создадим сетку для моделирования речной сети
    x_coords = [x_min + i * dx for i in range(int((x_max - x_min) / dx))]
    y_coords = [y_min + i * dy for i in range(int((y_max - y_min) / dy))]

    # Создадим сетку для моделирования речной сети
    network_gdf = gpd.GeoDataFrame(geometry=[shape({'type': 'Polygon', 
                                                     'coordinates': [[(x, y), (x + dx, y), (x + dx, y + dy), (x, y + dy), (x, y)] for x, y in zip(x_coords, y_coords)]]})])

    return network_gdf

# Применим алгоритм для определения конфигурации речной сети
network_gdf = create_network(gdf_tekes, gdf_sarykan)

# Визуализируем результат на карте с помощью библиотеки Folium
m = folium.Map(location=[gdf_tekes.centroid.y, gdf_sarykan.centroid.x], zoom_start=10)
folium.GeoJson(network_gdf.to_crs(epsg=3857).to_json(), name='network').add_to(m)

# Сохраним карту в файл
m.save("180.html")