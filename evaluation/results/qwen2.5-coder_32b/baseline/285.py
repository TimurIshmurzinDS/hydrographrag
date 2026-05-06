import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import yfinance as yf
import folium

# Шаг 1: Сбор и подготовка данных
def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'
data = download_data(ticker, start_date, end_date)

# Шаг 2: Реализация стратегий трейдинга
def moving_average_strategy(data, short_window=40, long_window=100):
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    
    return signals

def rsi_strategy(data, period=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['rsi'] = rsi
    
    signals['signal'][period:] = np.where(signals['rsi'][period:] < 30, 1.0, 0.0)
    signals['signal'][period:] = np.where(signals['rsi'][period:] > 70, -1.0, signals['signal'][period:])
    
    signals['positions'] = signals['signal'].diff()
    
    return signals

# Применение стратегий
ma_signals = moving_average_strategy(data)
rsi_signals = rsi_strategy(data)

# Шаг 3: Эксплуатация моделей и анализ результатов
def backtest_strategy(signals, data):
    initial_capital = float(10000.0)
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    portfolio = pd.DataFrame(index=signals.index).fillna(0.0)

    positions[ticker] = signals['signal']
    portfolio['positions'] = (positions.multiply(data['Close'], axis=0))
    pos_diff = positions.diff()
    
    portfolio['holdings'] = (positions.multiply(data['Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Close'], axis=0)).sum(axis=1).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()

    return portfolio

ma_portfolio = backtest_strategy(ma_signals, data)
rsi_portfolio = backtest_strategy(rsi_signals, data)

# Шаг 4: Визуализация данных
plt.figure(figsize=(12,6))
plt.plot(data.index, ma_portfolio['total'], label='MA Strategy')
plt.plot(data.index, rsi_portfolio['total'], label='RSI Strategy')
plt.title('Backtest Results')
plt.xlabel('Date')
plt.ylabel('Total Portfolio Value')
plt.legend()
plt.show()

# Визуализация на карте (пример: если у нас есть географические данные)
# Здесь мы просто создадим карту без реальных данных, так как в задаче нет указания на использование геоданных
m = folium.Map(location=[55.755826, 37.6173], zoom_start=10) # Координаты Москвы для примера
folium.Marker([55.755826, 37.6173]).add_to(m)
m.save("285.html")