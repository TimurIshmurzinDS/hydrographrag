import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о сезонном расходе реки Или.
# Файл содержит столбцы 'Date' и 'Discharge', где Discharge - это расход воды в кубических метрах в секунду.

data = pd.read_csv('discharge_data.csv', parse_dates=['Date'], index_col='Date')

# Шаг 2: Обработка данных
# Проверка пропущенных значений и удаление их, если они есть.
data.dropna(inplace=True)

# Создание новых признаков для моделирования (например, месяц года)
data['Month'] = data.index.month

# Шаг 3: Моделирование
# Используем линейную регрессию для предсказания расхода воды по месяцам.
X = data[['Month']]
y = data['Discharge']

model = LinearRegression()
model.fit(X, y)

# Предсказание расхода воды на каждый месяц года
months = np.arange(1, 13).reshape(-1, 1)
predicted_discharge = model.predict(months)

# Шаг 4: Оптимизация местоположения майнинговой станции
# Предположим, что оптимальное место для установки майнинговой станции - это месяц с максимальным расходом воды.
optimal_month = months[np.argmax(predicted_discharge)][0]
print(f"Оптимальный месяц для майнинга: {optimal_month}")

# Шаг 5: Визуализация
# Создание карты с отображением реки Или и выбранного места для майнинга.
m = folium.Map(location=[42.03, 21.76], zoom_start=9)  # Координаты примерно посередине реки Или

# Добавление маркера на карту (примерные координаты для оптимального места)
folium.Marker(
    location=[42.03, 21.76],  # Здесь должны быть реальные координаты
    popup=f"Оптимальное место для майнинга в {optimal_month} месяце",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты в HTML файл
m.save("227.html")

# Визуализация предсказанных данных о расходе воды
plt.figure(figsize=(10, 6))
plt.plot(data.index.month, data['Discharge'], label='Исторические данные')
plt.plot(months, predicted_discharge, label='Предсказанные данные', linestyle='--')
plt.xlabel('Месяц')
plt.ylabel('Расход воды (куб. м/с)')
plt.title('Сезонный расход воды реки Или')
plt.legend()
plt.show()