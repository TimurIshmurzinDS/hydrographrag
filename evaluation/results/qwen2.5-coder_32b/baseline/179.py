import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import folium
from shapely.geometry import Point, LineString

# Загрузка данных о речной сети (примерный путь к файлу)
river_network = gpd.read_file('path_to_river_network.shp')

# Фильтрация реки Киши-Осек из речной сети
kishi_oshek = river_network[river_network['name'] == 'Киши-Осек']

# Загрузка DEM (примерный путь к файлу)
with rasterio.open('path_to_dem.tif') as src:
    dem = src.read(1)
    transform = src.transform

# Маскирование DEM по границам реки Киши-Осек
geoms = [kishi_oshek.geometry.iloc[0]]
out_image, out_transform = mask(src, geoms, crop=True)

# Простая модель распространения паводка (пример)
def flood_spread(dem_array):
    flooded_area = np.zeros_like(dem_array, dtype=bool)
    start_points = [(i, j) for i in range(dem_array.shape[0]) for j in range(dem_array.shape[1]) if dem_array[i, j] < 200]
    
    for x, y in start_points:
        flooded_area[x, y] = True
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for nx, ny in neighbors:
            if 0 <= nx < dem_array.shape[0] and 0 <= ny < dem_array.shape[1]:
                if not flooded_area[nx, ny] and dem_array[nx, ny] < 250:
                    flooded_area[nx, ny] = True
    return flooded_area

flooded_area = flood_spread(out_image)

# Преобразование массива паводковых зон в геометрические объекты
def array_to_polygons(array, transform):
    polygons = []
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i, j]:
                x, y = rasterio.transform.xy(transform, i, j)
                polygons.append(Point(x, y))
    return gpd.GeoDataFrame(geometry=polygons)

flooded_polygons = array_to_polygons(flooded_area, out_transform)

# Визуализация на карте с использованием folium
m = folium.Map(location=[kishi_oshek.geometry.centroid.y.iloc[0], kishi_oshek.geometry.centroid.x.iloc[0]], zoom_start=12)
folium.GeoJson(kishi_oshek).add_to(m)

# Добавление паводковых зон на карту
for _, row in flooded_polygons.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=2,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

m.save("179.html")