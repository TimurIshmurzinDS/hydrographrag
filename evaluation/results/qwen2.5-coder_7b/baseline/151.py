import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Загрузка данных о топографии (например, из shapefile)
topography_data = gpd.read_file('path_to_topography_shapefile.shp')

# Загрузка данных о климате (например, из CSV файла)
climate_data = pd.read_csv('path_to_climate_data.csv')

# Пример данных климатических условий
# climate_data.columns = ['latitude', 'longitude', 'precipitation', 'temperature', 'humidity']

# Создание геометрии точек для климатических данных
geometry = [Point(xy) for xy in zip(climate_data['longitude'], climate_data['latitude'])]
climate_gdf = gpd.GeoDataFrame(climate_data, geometry=geometry)

# Объединение данных топографии и климатических условий
merged_data = gpd.sjoin(topography_data, climate_gdf, how="left", op='within')

# Оценка риска паводков (пример простой модели)
merged_data['risk'] = merged_data['precipitation'] * merged_data['temperature']

# Создание карты
m = folium.Map(location=[40.7128, -74.0060], zoom_start=5)

# Добавление слоя топографии
folium.GeoJson(topography_data).add_to(m)

# Добавление слоя риска паводков
risk_layer = folium.FeatureGroup(name='Risk of Flooding')
for idx, row in merged_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['risk'] / 100,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.5
    ).add_to(risk_layer)

risk_layer.add_to(m)

# Добавление слоя управления слоями
folium.LayerControl().add_to(m)

# Сохранение карты
m.save("151.html")