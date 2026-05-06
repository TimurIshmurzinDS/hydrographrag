import geopandas as gpd
from shapely.geometry import Polygon
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import folium

# Загрузка данных о реках
saraykan_gdf = gpd.read_file('path_to_saraykan_shapefile.shp')
emel_gdf = gpd.read_file('path_to_emel_shapefile.shp')

# Выделение бассейнов (пример с использованием алгоритма D8)
from rios import applier
from osgeo import gdal, ogr

def extract_basins(raster_path, vector_path):
    # Загрузка растра и вектора
    raster = gdal.Open(raster_path)
    vector = ogr.Open(vector_path)

    # Создание выходного векторного файла
    driver = ogr.GetDriverByName("ESRI Shapefile")
    out_vector = driver.CreateDataSource('output_basins.shp')
    out_layer = out_vector.CreateLayer('basins', geom_type=ogr.wkbPolygon)

    # Определение полей для выходного вектора
    field_defn = ogr.FieldDefn('ID', ogr.OFTInteger)
    out_layer.CreateField(field_defn)

    # Применение алгоритма D8
    applier.apply(process, raster, vector, output=out_vector)

def process(raster, vector):
    # Здесь нужно реализовать алгоритм выделения бассейнов (например, алгоритм D8)
    # В качестве примера создадим простой полигон для каждой реки
    saraykan_polygon = Polygon([(0, 0), (1, 1), (2, 0)])
    emel_polygon = Polygon([(3, 3), (4, 4), (5, 3)])

    # Создание геометрий и запись в выходной вектор
    saraykan_feature = ogr.Feature(out_layer.GetLayerDefn())
    saraykan_feature.SetGeometry(saraykan_polygon)
    out_layer.CreateFeature(saraykan_feature)

    emel_feature = ogr.Feature(out_layer.GetLayerDefn())
    emel_feature.SetGeometry(emel_polygon)
    out_layer.CreateFeature(emel_feature)

# Вызов функции для выделения бассейнов
extract_basins('path_to_raster.tif', 'path_to_vector.shp')

# Загрузка данных о бассейнах
basins_gdf = gpd.read_file('output_basins.shp')

# Оценка топологической сложности
def calculate_topological_complexity(gdf):
    complexity = {}
    for index, row in gdf.iterrows():
        area = row.geometry.area
        length = row.geometry.length
        num_inlets = len(row.geometry.interiors)
        complexity[index] = {
            'area': area,
            'length': length,
            'num_inlets': num_inlets
        }
    return complexity

saraykan_complexity = calculate_topological_complexity(saraykan_gdf)
emel_complexity = calculate_topological_complexity(emel_gdf)

# Вывод результатов
print("Топологическая сложность бассейна рек Сарыкан:")
for key, value in saraykan_complexity.items():
    print(f"ID: {key}, Площадь: {value['area']}, Длина: {value['length']}, Количество впадин: {value['num_inlets']}")

print("\nТопологическая сложность бассейна рек Эмель:")
for key, value in emel_complexity.items():
    print(f"ID: {key}, Площадь: {value['area']}, Длина: {value['length']}, Количество впадин: {value['num_inlets']}")

# Визуализация на карте
m = folium.Map(location=[saraykan_gdf.geometry.centroid.y.mean(), saraykan_gdf.geometry.centroid.x.mean()], zoom_start=10)

for index, row in basins_gdf.iterrows():
    if 'Saraykan' in row['ID']:
        folium.Polygon(row.geometry, color='blue', fill=True, fill_color='blue').add_to(m)
    elif 'Emel' in row['ID']:
        folium.Polygon(row.geometry, color='red', fill=True, fill_color='red').add_to(m)

m.save("177.html")