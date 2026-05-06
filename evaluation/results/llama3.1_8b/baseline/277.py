import pandas as pd
import yfinance as yf
from folium import Map, Marker
import matplotlib.pyplot as plt

# Шаг 1: Сбор данных о ценах и объемах торгов акций технологических компаний за последние 30 лет.
tech_stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'FB']
data = {}
for stock in tech_stocks:
    ticker = yf.Ticker(stock)
    hist = ticker.history(period='30y')
    data[stock] = hist

# Шаг 2: Обработка данных для исключения пропусков и аномалий.
for stock, hist in data.items():
    hist.dropna(inplace=True)

# Шаг 3: Создание индекса прибыльности на основе изменений цен и объемов торгов.
def calculate_profitability(hist):
    return (hist['Close'] - hist['Open']) / hist['Open']

profitabilities = {}
for stock, hist in data.items():
    profit = calculate_profitability(hist)
    profitabilities[stock] = profit

# Шаг 4: Анализ показателей прибыльности по годам и сравнение с общими рыночными тенденциями.
years = list(range(1990, 2023))
profitability_index = {}
for year in years:
    profitability_year = []
    for stock, profit in profitabilities.items():
        profitability_year.append(profit[year])
    profitability_index[year] = sum(profitability_year) / len(profitability_year)

# Визуализация результатов на карте
m = Map(location=[37.7749, -122.4194], zoom_start=12)
for stock, hist in data.items():
    marker = Marker(location=[37.7749, -122.4194], popup=f'{stock}').add_to(m)

# Сравнение прибыльности по годам
plt.plot(years, list(profitability_index.values()))
plt.xlabel('Год')
plt.ylabel('Процент прибыльности')
plt.title('Сравнение прибыльности акций технологического сектора за последние 30 лет')
plt.show()

# Сохранение карты в файл
m.save("277.html")