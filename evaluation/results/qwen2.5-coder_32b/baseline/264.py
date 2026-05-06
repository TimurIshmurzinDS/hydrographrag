import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с историческими данными о уровне воды и стоимости токенов
data = pd.read_csv('bayankol_water_level_and_token_prices.csv', parse_dates=['date'])

# Шаг 2: Предварительная обработка данных
# Проверка на пропуски
print(data.isnull().sum())

# Удаление строк с пропусками
data.dropna(inplace=True)

# Преобразование временных рядов к нужному формату
data.set_index('date', inplace=True)

# Шаг 3: Анализ данных
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))
plt.plot(data['water_level'], label='Уровень воды')
plt.plot(data['token_price'], label='Стоимость токенов')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.title('Исторические данные уровня воды и стоимости токенов')
plt.legend()
plt.show()

# Шаг 4: Моделирование
X = data[['water_level']]
y = data['token_price']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Шаг 5: Оценка модели
mse = mean_squared_error(y_test, y_pred)
print(f'Средняя квадратическая ошибка (MSE): {mse}')

# Шаг 6: Визуализация результатов
# Предположим, что у нас есть координаты реки Баянколь
bayankol_coords = [42.8743, 80.9499]

# Создание карты с помощью folium
m = folium.Map(location=bayankol_coords, zoom_start=10)

# Добавление маркера на карте
folium.Marker(
    location=bayankol_coords,
    popup='Река Баянколь',
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в HTML файл
m.save("264.html")

# Визуализация прогнозированных значений на тестовой выборке
plt.figure(figsize=(14, 7))
plt.plot(y_test.values, label='Фактические значения')
plt.plot(y_pred, label='Прогнозные значения')
plt.xlabel('Наблюдения')
plt.ylabel('Стоимость токенов')
plt.title('Сравнение фактических и прогнозированных значений стоимости токенов')
plt.legend()
plt.show()