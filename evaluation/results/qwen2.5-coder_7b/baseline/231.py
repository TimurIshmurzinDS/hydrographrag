import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Загрузка данных
data = pd.read_csv('koktal_water_levels.csv')

# Предварительный анализ данных
print(data.head())
print(data.describe())

# Построение модели линейной регрессии
X = data['date'].values.reshape(-1, 1)
y = data['water_level'].values

model = LinearRegression()
model.fit(X, y)

# Предсказание водных уровней на основе модели
data['predicted_water_level'] = model.predict(X)

# Визуализация данных на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f"Date: {row['date']}, Water Level: {row['water_level']:.2f} m, Predicted: {row['predicted_water_level']:.2f} m",
                  icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("231.html")