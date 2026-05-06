import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# 1. Сбор и предобработка данных (замените 'data.csv' на ваш файл)
data = pd.read_csv('data.csv', index_col='Date', parse_dates=True)

# 2. Выбор модели (здесь используется линейная регрессия)
model = LinearRegression()

# 3. Обучение модели
X = data.index.astype(int).values.reshape(-1, 1)  # Преобразовать даты в числовой формат
y = data['WaterLevel'].values
model.fit(X, y)

# 4. Прогнозирование
future_dates = pd.date_range(start='2024-01-01', end='2024-12-31')
future_dates_numeric = future_dates.astype(int).values.reshape(-1, 1)
predicted_water_levels = model.predict(future_dates_numeric)

# 5. Визуализация (предполагается, что у вас есть координаты реки Batareyka)
m = folium.Map(location=[latitude, longitude], zoom_start=12)
folium.PolyLine(locations=river_coordinates, color='blue').add_to(m)

# Добавить прогнозные значения на карту (необходимо реализовать)

m.save("55.html")