import pandas as pd
from folium import Map, Marker
import geopandas as gpd
from shapely.geometry import Point

# Сбор и подготовка данных о уровнях воды в реках
data = {
    'river': ['Ili River', 'Karatal River'],
    'water_level': [10.5, 8.2]
}
df = pd.DataFrame(data)

# Подготовка геоданных для Ili River и Karatal River
ili_gdf = gpd.read_file('path_to_ili_river.shp')
karatal_gdf = gpd.read_file('path_to_karatal_river.shp')

# Создание рasters с данными о уровнях воды в реках
from rasterio import features
from rasterio.io import MemoryFile

with MemoryFile() as memfile:
    with memfile.get_driver().open(
        driver='GTiff',
        height=ili_gdf.shape[0],
        width=ili_gdf.shape[1],
        count=1,
        dtype='float32'
    ) as dataset:
        features.rasterize(
            ili_gdf.geometry, 
            out_shape=(ili_gdf.shape[0], ili_gdf.shape[1]),
            fill=-9999.0,
            transform=dataset.transform,
            out=dataset.read(1)
        )
        
        with memfile.get_root().open() as src:
            raster = src.read(1)

# Анализ данных: определение текущего уровня воды в реках
current_water_level_ili = df.loc[df['river'] == 'Ili River', 'water_level'].values[0]
current_water_level_karatal = df.loc[df['river'] == 'Karatal River', 'water_level'].values[0]

# Визуализация результатов на карте с помощью библиотеки Folium
m = Map(location=[46.5, 76.5], zoom_start=10)
Marker([ili_gdf.geometry.centroid.y, ili_gdf.geometry.centroid.x],
       popup='Текущий уровень воды в реке Ili River: ' + str(current_water_level_ili)).add_to(m)
Marker([karatal_gdf.geometry.centroid.y, karatal_gdf.geometry.centroid.x],
       popup='Текущий уровень воды в реке Karatal River: ' + str(current_water_level_karatal)).add_to(m)

m.save("9.html")