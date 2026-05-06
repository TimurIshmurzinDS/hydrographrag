import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных
data = pd.read_csv('uzyn_kargaly_water_levels.csv')

# Шаг 2: Очистка данных
data = data.dropna()

# Шаг 3: Анализ данных
X = np.array(data['date']).reshape(-1, 1)
y = np.array(data['water_level'])

model = LinearRegression()
model.fit(X, y)

# Шаг 4: Моделирование
predicted_water_level = model.predict(np.array([max(data['date'])]).reshape(-1, 1))

# Шаг 5: Валидация модели (в данном примере не реализована)

# Шаг 6: Визуализация результатов
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
folium.Marker([data['latitude'], data['longitude']], popup=f'Пиковый уровень воды: {predicted_water_level[0]} м').add_to(m)

m.save("22.html")