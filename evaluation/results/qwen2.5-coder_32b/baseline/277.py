import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
# Выберем несколько компаний из технологического сектора
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB']
start_date = '2013-01-01'
end_date = '2023-01-01'

# Загрузка данных о ценах акций
data = yf.download(tech_stocks, start=start_date, end=end_date)['Adj Close']

# Шаг 2: Обработка данных
# Проверка на пропущенные значения и заполнение их средним значением
data.fillna(method='ffill', inplace=True)

# Шаг 3: Анализ прибыльности
# Расчет процентной доходности
returns = data.pct_change().dropna()

# Средняя доходность и стандартное отклонение
mean_returns = returns.mean()
std_devs = returns.std()

# Шаг 4: Визуализация результатов
plt.figure(figsize=(12, 6))
plt.plot(returns.index, returns)
plt.title('Процентная доходность акций технологического сектора')
plt.xlabel('Дата')
plt.ylabel('Процентная доходность')
plt.legend(tech_stocks)
plt.grid(True)
plt.show()

# Вывод средней доходности и стандартного отклонения
summary_stats = pd.DataFrame({'Средняя доходность': mean_returns, 'Стандартное отклонение': std_devs})
print(summary_stats)

# Шаг 5: Географическая визуализация (опционально)
# Координаты компаний из технологического сектора
company_coords = {
    'AAPL': [37.3348, -122.0089],  # Apple Inc.
    'MSFT': [47.6740, -122.1215],  # Microsoft Corporation
    'GOOGL': [37.4220, -122.0841], # Alphabet Inc. (Google)
    'AMZN': [39.6136, -105.0167], # Amazon.com, Inc.
    'FB': [37.4851, -122.1481]   # Meta Platforms, Inc. (Facebook)
}

# Создание карты
m = folium.Map(location=[39.5, -98.35], zoom_start=4)

# Добавление маркеров на карту
for company, coords in company_coords.items():
    folium.Marker(
        location=coords,
        popup=f'{company} ({mean_returns[company]:.2%} средняя доходность)',
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("277.html")