import pandas as pd
import yfinance as yf
import folium

# Получение данных о ценах акций
tickers = ['AAPL', 'MSFT', 'GOOG']
data = yf.download(tickers, start='1993-01-01', end='2023-01-01')

# Расчет процентной прибыльности
returns = data['Adj Close'].pct_change() * 100

# Создание карты Folium
m = folium.Map(location=[40, -75], zoom_start=4)

# Добавление маркеров на карту с графиками прибыльности
for ticker in tickers:
    company_data = yf.Ticker(ticker).info
    lat = company_data['latitude']
    lon = company_data['longitude']
    folium.Marker([lat, lon], popup=f'{ticker}').add_to(m)

    # Добавление графика прибыльности на маркер
    chart_data = returns[ticker].dropna()
    chart = folium.plugins.Chart(location=[lat + 0.1, lon], data=chart_data.values.tolist())
    chart.add_to(m)

# Сохранение карты
m.save("277.html")