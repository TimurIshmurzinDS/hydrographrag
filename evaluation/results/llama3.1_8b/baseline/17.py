import pandas as pd
from folium import Map, Marker
import geopandas as gpd

# Сбор и очистка данных (предположим, что данные находятся в файле 'water_data.csv')
data = pd.read_csv('water_data.csv')

# Геопространственное преобразование данных
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['long'], data['lat']))

# Создание модели (предположим, что мы используем простую линейную регрессию)
from sklearn.linear_model import LinearRegression

X = gdf[['long', 'lat']]
y = gdf['water_flow']

model = LinearRegression()
model.fit(X, y)

# Визуализация результатов
m = Map(location=[46.5, 68.0], zoom_start=10)
for index, row in data.iterrows():
    marker = Marker(location=[row['lat'], row['long']], popup=f'Расход воды: {row["water_flow"]} м³/с')
    m.add_child(marker)

# Визуализация весеннего расхода воды
spring_data = data[data['season'] == 'весна']
for index, row in spring_data.iterrows():
    marker = Marker(location=[row['lat'], row['long']], popup=f'Расход воды в весну: {row["water_flow"]} м³/с')
    m.add_child(marker)

# Сохранение карты
m.save("17.html")