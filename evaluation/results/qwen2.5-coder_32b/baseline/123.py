import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файлы с данными о уровнях воды для рек Kurty и Sharyn.
kurty_data = pd.read_csv('kurty_water_level.csv', parse_dates=['date'])
sharyn_data = pd.read_csv('sharyn_water_level.csv', parse_dates=['date'])

# Шаг 2: Предварительная обработка данных
# Очистка пропусков и нормализация временных рядов
kurty_data.dropna(inplace=True)
sharyn_data.dropna(inplace=True)

# Выравнивание временных рядов по дате
merged_data = pd.merge(kurty_data, sharyn_data, on='date', suffixes=('_kurty', '_sharyn'))

# Шаг 3: Анализ трендов
# Используем метод линейной регрессии для анализа тренда
from sklearn.linear_model import LinearRegression

X_kurty = np.array(merged_data.index).reshape(-1, 1)
y_kurty = merged_data['water_level_kurty']
model_kurty = LinearRegression().fit(X_kurty, y_kurty)

X_sharyn = np.array(range(len(sharyn_data))).reshape(-1, 1)  # Предполагаем, что данные Sharyn у нас полные
y_sharyn = sharyn_data['water_level']
model_sharyn = LinearRegression().fit(X_sharyn, y_sharyn)

# Шаг 4: Сравнение трендов
# Используем коэффициент корреляции Пирсона для сравнения трендов
correlation, _ = pearsonr(model_kurty.predict(X_kurty), model_sharyn.predict(X_sharyn))
print(f"Коэффициент корреляции между трендами: {correlation}")

# Шаг 5: Визуализация результатов
# Предположим, что у нас есть координаты рек для визуализации на карте
kurty_coords = (42.874369, 78.251031)  # Примерные координаты Kurty River
sharyn_coords = (42.855333, 78.241167)  # Примерные координаты Sharyn River

m = folium.Map(location=[(kurty_coords[0] + sharyn_coords[0]) / 2, 
                         (kurty_coords[1] + sharyn_coords[1]) / 2], zoom_start=10)

folium.Marker(kurty_coords, popup='Kurty River').add_to(m)
folium.Marker(sharyn_coords, popup='Sharyn River').add_to(m)

# Добавление линии между точками рек
folium.PolyLine([kurty_coords, sharyn_coords], color="blue", weight=2.5, opacity=1).add_to(m)

m.save("123.html")