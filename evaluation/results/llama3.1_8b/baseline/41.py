import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Сбор данных о фермерских хозяйствах и их местоположении
data = {
    'name': ['Хозяйство 1', 'Хозяйство 2', 'Хозяйство 3'],
    'lat': [55.123, 55.456, 55.789],
    'lon': [82.345, 82.678, 83.012]
}
df = pd.DataFrame(data)

# Получение данных о расходе воды на эти хозяйства
water_consumption = {
    'name': ['Хозяйство 1', 'Хозяйство 2', 'Хозяйство 3'],
    'consumption': [100, 200, 300]
}
df_water = pd.DataFrame(water_consumption)

# Геообработка данных для определения расстояния от реки Аксу до каждого хозяйства
def calculate_distance(lat1, lon1, lat2, lon2):
    import math
    R = 6371  # радиус Земли в км
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

df['distance'] = df.apply(lambda row: calculate_distance(row['lat'], row['lon'], 55.123, 82.345), axis=1)

# Создание модели, которая связывает потребление воды с географическими координатами
import numpy as np
from sklearn.linear_model import LinearRegression

X = df[['distance']]
y = df_water['consumption']

model = LinearRegression()
model.fit(X, y)

# Визуализация результатов на карте
m = Map(location=[55.123, 82.345], zoom_start=10)
for index, row in df.iterrows():
    Marker(location=[row['lat'], row['lon']], popup=f'Хозяйство: {row["name"]}, Расстояние: {row["distance"]} км').add_to(m)

HeatMap(data=df[['lat', 'lon']].values.tolist(), radius=10).add_to(m)
m.save("41.html")