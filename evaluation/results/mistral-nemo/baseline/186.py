import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Подготовка данных
water_quality_data = pd.read_csv('water_quality.csv')
agriculture_data = pd.read_csv('agriculture.csv')

# Очистка и преобразование данных для дальнейшего анализа
water_quality_data = water_quality_data.dropna()
agriculture_data = agriculture_data.dropna()

# 2. Геопространственный анализ
gdf_water = gpd.GeoDataFrame(water_quality_data, geometry=gpd.points_from_xy(water_quality_data['longitude'], water_quality_data['latitude']))
gdf_agri = gpd.GeoDataFrame(agriculture_data, geometry=gpd.points_from_xy(agriculture_data['longitude'], agriculture_data['latitude']))

# Преобразование в систему координат WGS84
gdf_water.crs = 'EPSG:4326'
gdf_agri.crs = 'EPSG:4326'

# Буферный анализ для определения зон влияния загрязнения реки Бутак на близлежащие сельскохозяйственные участки
buffer_distance = 500 # примерное расстояние в метрах
gdf_agri['geometry'] = gdf_agri.buffer(buffer_distance)

# 3. Анализ качества воды
# Сопоставьте данные о качестве воды с данными о сельскохозяйственных участках для определения влияния загрязнения на качество воды, используемую в сельском хозяйстве

# 4. Визуализация результатов
m = folium.Map(location=[water_quality_data['latitude'].mean(), water_quality_data['longitude'].mean()], zoom_start=10)

# Отобразите зоны влияния загрязнения реки Бутак и качество воды на сельскохозяйственных участках
for idx, row in gdf_water.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=5,
                        color='blue',
                        fill=True,
                        fill_opacity=0.5).add_to(m)

for idx, row in gdf_agri.iterrows():
    folium.Polygon(locations=[(point.y, point.x) for point in row['geometry'].exterior.coords],
                   color='green',
                   weight=2,
                   fill=True,
                   fill_opacity=0.5).add_to(m)

# Сохраните финальную карту как "186.html"
m.save("186.html")