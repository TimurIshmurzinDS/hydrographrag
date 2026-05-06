import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Пример данных о уровне воды в реке Или (замените на реальные данные)
data = {
    'date': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05'],
    'water_level': [100, 102, 98, 101, 103],
    'temperature': [20, 22, 21, 23, 24],
    'precipitation': [0.5, 0.7, 0.6, 0.8, 0.9]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Преобразование даты в числовой формат для моделирования
df['date_num'] = (df['date'] - df['date'].min()).dt.days

# Разделение данных на признаки и целевую переменную
X = df[['temperature', 'precipitation', 'date_num']]
y = df['water_level']

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# Прогнозирование уровня воды на основе текущих данных
current_data = {
    'temperature': [23],
    'precipitation': [0.8],
    'date_num': [(df['date'].max() - pd.to_datetime('2023-10-05')).days]
}
current_df = pd.DataFrame(current_data)
predicted_water_level = model.predict(current_df)

# Визуализация данных на карте
m = folium.Map(location=[47.86, 91.77], zoom_start=10)  # Координаты примера для реки Или

for index, row in df.iterrows():
    folium.Marker([47.86, 91.77], popup=f"Уровень воды: {row['water_level']}, Дата: {row['date']}").add_to(m)

folium.Marker([47.86, 91.77], popup=f"Прогнозируемый уровень воды: {predicted_water_level[0]:.2f}").add_to(m)

m.save("31.html")