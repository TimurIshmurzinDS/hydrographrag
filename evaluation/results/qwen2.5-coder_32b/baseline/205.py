import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два CSV файла: 'snowmelt_dates.csv' и 'discharge_data.csv'
# snowmelt_dates.csv содержит столбцы: date (дата), snowmelt_date (дата снеготаяния)
# discharge_data.csv содержит столбцы: date (дата), discharge (стока реки)

snowmelt_df = pd.read_csv('snowmelt_dates.csv', parse_dates=['date', 'snowmelt_date'])
discharge_df = pd.read_csv('discharge_data.csv', parse_dates=['date'])

# Шаг 2: Предварительная обработка данных
# Выравнивание временных рядов по дате
merged_df = pd.merge(snowmelt_df, discharge_df, on='date')
merged_df.dropna(inplace=True)

# Преобразование даты снеготаяния в количество дней от начала года
merged_df['snowmelt_day_of_year'] = merged_df['snowmelt_date'].dt.dayofyear

# Шаг 3: Анализ временных рядов
# Проверка стационарности временных рядов
def test_stationarity(timeseries):
    result = adfuller(timeseries, autolag='AIC')
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])

test_stationarity(merged_df['snowmelt_day_of_year'])
test_stationarity(merged_df['discharge'])

# Шаг 4: Моделирование взаимосвязи
# Использование линейной регрессии для анализа зависимости стока от срока снеготаяния
X = merged_df[['snowmelt_day_of_year']]
y = merged_df['discharge']

model = LinearRegression()
model.fit(X, y)

# Предсказание и оценка модели
predictions = model.predict(X)
plt.figure(figsize=(10, 6))
plt.scatter(merged_df['snowmelt_day_of_year'], merged_df['discharge'], color='blue', label='Actual')
plt.plot(merged_df['snowmelt_day_of_year'], predictions, color='red', linewidth=2, label='Predicted')
plt.xlabel('День снеготаяния в году')
plt.ylabel('Сток реки Лепси')
plt.title('Зависимость стока реки от дня снеготаяния')
plt.legend()
plt.show()

# Шаг 5: Визуализация результатов
# Создание карты для демонстрации местоположения реки Лепси (координаты примерные)
m = folium.Map(location=[43.20, 76.92], zoom_start=10)

# Добавление маркера на карте
folium.Marker(
    location=[43.20, 76.92],
    popup='Река Лепси',
    icon=folium.Icon(icon="info-sign")
).add_to(m)

m.save("205.html")

# Вывод коэффициентов модели
print(f'Коэффициент наклона: {model.coef_[0]}')
print(f'Свободный член: {model.intercept_}')