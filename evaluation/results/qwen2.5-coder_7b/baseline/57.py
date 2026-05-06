import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('kurty_river_water_level.csv')

# Предположим, что данные имеют столбцы 'date' и 'water_level'
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Построение модели линейной регрессии
X = data.index.values.reshape(-1, 1)
y = data['water_level'].values

model = LinearRegression()
model.fit(X, y)

# Прогнозирование будущих значений
future_dates = pd.date_range(start=data.index[-1], periods=30, freq='D')
future_X = future_dates.values.reshape(-1, 1)
predicted_water_levels = model.predict(future_X)

# Визуализация данных и прогноза на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Добавление точек с историческими данными
for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Date: {index.strftime('%Y-%m-%d')}, Water Level: {row['water_level']}", icon=folium.Icon(color='blue')).add_to(m)

# Добавление точек с прогнозируемыми данными
for date, level in zip(future_dates, predicted_water_levels):
    folium.Marker([data['latitude'].mean(), data['longitude'].mean()], popup=f"Predicted Date: {date.strftime('%Y-%m-%d')}, Predicted Water Level: {level}", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("57.html")