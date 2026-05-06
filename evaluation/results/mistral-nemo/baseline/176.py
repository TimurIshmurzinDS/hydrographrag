import geopandas as gpd
from shapely.geometry import Point
from sklearn.neighbors import NearestNeighbors
import numpy as np
import folium

# 1. Загрузить данные о русле ручья Терисбутак и реки Талгар в формате векторных данных (например, Shapefile)
terisbutak = gpd.read_file("terisbutak.shp")
talgar = gpd.read_file("talgar.shp")

# 2. Преобразовать векторные данные в растровые с помощью функции интерполяции
def rasterize_data(gdf):
    geometries = [geom for geom in gdf.geometry]
    coordinates = np.array([[geom.x, geom.y] for geom in geometries])
    nbrs = NearestNeighbors(n_neighbors=1).fit(coordinates)
    distances, _ = nbrs.kneighbors(coordinates)
    return distances

terisbutak_raster = rasterize_data(terisbutak)
talgar_raster = rasterize_data(talgar)

# 3. Вычислить расстояние между каждой точкой русла ручья Терисбутак и реки Талгар с использованием функции расстояния
def calculate_distances(terisbutak_raster, talgar_raster):
    distances = np.zeros(len(terisbutak_raster))
    for i in range(len(terisbutak_raster)):
        distances[i] = np.min(np.abs(talgar_raster - terisbutak_raster[i]))
    return distances

distances = calculate_distances(terisbutak_raster, talgar_raster)

# 4. Создать матрицу близости
proximity_matrix = pd.DataFrame({'Terisbutak': terisbutak['id'], 'Distance_to_Talgar': distances})

# 5. Визуализировать результаты анализа на карте с использованием библиотеки `folium`
m = folium.Map(location=[terisbutak.geometry.y.mean(), terisbutak.geometry.x.mean()], zoom_start=12)

for _, row in proximity_matrix.iterrows():
    folium.CircleMarker(
        location=(row['geometry'].x, row['geometry'].y),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

m.save("176.html")