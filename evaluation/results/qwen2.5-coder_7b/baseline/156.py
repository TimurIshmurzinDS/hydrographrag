import geopandas as gpd
import folium
from shapely.geometry import Polygon, Point
import numpy as np

# Загрузка данных
ili_river = gpd.read_file("path_to_ili_river.shp")
sarykan_river = gpd.read_file("path_to_sarykan_river.shp")
shynzhaly_river = gpd.read_file("path_to_shynzhaly_river.shp")

# Объединение данных
combined_rivers = ili_river.append([sarykan_river, shynzhaly_river])

# Создание сетки для анализа
minx, miny, maxx, maxy = combined_rivers.total_bounds
grid_size = 1000  # Размер ячейки в метрах
grid_x = np.arange(minx, maxx, grid_size)
grid_y = np.arange(miny, maxy, grid_size)

# Создание геометрий сетки
grid_cells = []
for x in grid_x:
    for y in grid_y:
        grid_cells.append(Polygon([(x, y), (x + grid_size, y), (x + grid_size, y + grid_size), (x, y + grid_size)]))

# Создание GeoDataFrame для сетки
grid_gdf = gpd.GeoDataFrame(geometry=grid_cells)

# Оценка площади затопления
def calculate_flooded_area(cell):
    # Здесь можно добавить логику для оценки площади затопления
    # Например, использовать модель паводков или данные о высоте над уровнем моря
    return np.random.randint(0, 10)  # Пример: случайное значение

grid_gdf['flooded_area'] = grid_gdf.geometry.apply(calculate_flooded_area)

# Визуализация результатов
m = folium.Map(location=[combined_rivers.centroid.y.mean(), combined_rivers.centroid.x.mean()], zoom_start=10)

for idx, row in grid_gdf.iterrows():
    if row['flooded_area'] > 0:
        folium.Rectangle(
            bounds=[[row.geometry.bounds[1], row.geometry.bounds[0]], [row.geometry.bounds[3], row.geometry.bounds[2]]],
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.5
        ).add_to(m)

for idx, row in combined_rivers.iterrows():
    folium.GeoJson(row.geometry).add_to(m)

m.save("156.html")