import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap
import geopandas as gpd
import matplotlib.pyplot as plt

# Подготовка данных
data_streamflow = pd.read_csv('streamflow_data.csv')
data_agroecosystems = pd.read_csv('agroecosystem_data.csv')

# Создание географической модели
gdf = gpd.GeoDataFrame(data_streamflow, geometry=gpd.points_from_xy(data_streamflow['longitude'], data_streamflow['latitude']))
buffer_gdf = gpd.GeoDataFrame(geometry=gdf.buffer(1000))

# Анализ сезонных колебаний стока реки Бутак
seasonal_trend = data_streamflow.groupby('month')['streamflow'].mean()

# Оценка влияния сезонных колебаний стока на устойчивость агроценозов
spatial_autocorrelation = gpd.sjoin(buffer_gdf, data_agroecosystems, how='inner', op='intersects')
correlation_matrix = spatial_autocorrelation.corr()

# Визуализация результатов
m = Map(location=[55.7558, 37.6173], zoom_start=10)
HeatMap(data_streamflow[['longitude', 'latitude', 'streamflow']].values, radius=20).add_to(m)

# Маркировка области с наибольшим риском деградации
max_risk_index = correlation_matrix['risk'].idxmax()
marker = Marker(location=[correlation_matrix.loc[max_risk_index]['latitude'], correlation_matrix.loc[max_risk_index]['longitude']], popup='Риск деградации: ' + str(correlation_matrix.loc[max_risk_index]['risk'])).add_to(m)

# Сохранение карты
m.save("192.html")