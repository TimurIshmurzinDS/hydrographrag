import pandas as pd
from folium import Map, CircleMarker
import matplotlib.pyplot as plt

# Шаг 1: Сбор данных о уровне воды в бассейнах рек за различные периоды времени.
# Для простоты предположим, что данные уже подготовлены и хранятся в двух таблицах:
# lepsy_data.csv и turgen_data.csv.

lepsy_data = pd.read_csv('lepsy_data.csv')
turgen_data = pd.read_csv('turgen_data.csv')

# Шаг 2: Подготовка данных к анализу: очистка, преобразование и объединение данных.
# Объединим данные двух таблиц по дате.

data = pd.concat([lepsy_data, turgen_data], ignore_index=True)

# Удалите пустые значения.

data.dropna(inplace=True)

# Шаг 3: Анализ долгосрочных трендов изменения уровня воды с помощью статистических методов.
# Используем линейную регрессию для каждого бассейна реки.

from sklearn.linear_model import LinearRegression

lepsy_level = data[data['river'] == 'Лепса']['level']
turgen_level = data[data['river'] == 'Тургуна']['level']

X_lepsy = range(len(lepsy_level))
X_turgen = range(len(turgen_level))

model_lepsy = LinearRegression()
model_lepsy.fit(X_lepsy.values.reshape(-1, 1), lepsy_level)

model_turgen = LinearRegression()
model_turgen.fit(X_turgen.values.reshape(-1, 1), turgen_level)

# Шаг 4: Визуализация результатов на карте с использованием библиотеки Folium.

m = Map(location=[50.0, 70.0], zoom_start=6)
lepsy_marker = CircleMarker([51.5, 69.2], radius=10).add_to(m)
turgen_marker = CircleMarker([52.1, 68.5], radius=10).add_to(m)

# Добавляем линии для каждого бассейна реки.

X_lepsy_pred = model_lepsy.predict(X_lepsy.values.reshape(-1, 1))
X_turgen_pred = model_turgen.predict(X_turgen.values.reshape(-1, 1))

folium.PolyLine([[51.5, 69.2], [51.5 + i * 0.01, 69.2 - model_lepsy.coef_[0] * i]] for i in range(len(lepsy_level))).add_to(m)
folium.PolyLine([[52.1, 68.5], [52.1 + j * 0.01, 68.5 - model_turgen.coef_[0] * j]] for j in range(len(turgen_level))).add_to(m)

m.save("198.html")