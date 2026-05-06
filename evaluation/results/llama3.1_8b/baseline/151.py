import pandas as pd
import numpy as np
from folium import Map, Marker, CircleMarker
from folium.plugins import HeatMap
import geopandas as gpd
from shapely.geometry import Point
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Сбор данных о реках и их бассейнах
bayankol_data = pd.read_csv('bayankol.csv')
ili_data = pd.read_csv('ili.csv')

# Объединение данных о реках в одну таблицу
rivers_data = pd.concat([bayankol_data, ili_data])

# Анализ исторических данных о паводках
pavodki_data = pd.read_csv('pavodki.csv')
pavodki_data['date'] = pd.to_datetime(pavodki_data['date'])
pavodki_data['level'] = pavodki_data['level'].astype(float)

# Создание модели риска паводков
X = pavodki_data[['temperature', 'precipitation', 'snowmelt']]
y = pavodki_data['level']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Анализ результатов моделирования
predictions = model.predict(X_test)

# Визуализация результатов на карте с помощью библиотеки Folium
m = Map(location=[46.5, 76], zoom_start=8)

for i in range(len(rivers_data)):
    lat = rivers_data.iloc[i]['lat']
    lon = rivers_data.iloc[i]['lon']
    risk_level = model.predict([[rivers_data.iloc[i]['temperature'], rivers_data.iloc[i]['precipitation'], rivers_data.iloc[i]['snowmelt']]])
    Marker(location=[lat, lon], popup=f'Риск паводка: {risk_level:.2f}').add_to(m)

HeatMap(data=rivers_data[['lat', 'lon']].values, radius=10).add_to(m)

m.save("151.html")