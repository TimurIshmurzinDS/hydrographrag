import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import folium

# Шаг 1: Сбор данных о уровне реки Аягоз
def fetch_water_level_data(start_date, end_date):
    # Предположим, что есть API для получения данных о уровне воды реки Аягоз
    url = "https://api.example.com/water-level"
    params = {
        'start': start_date.strftime('%Y-%m-%d'),
        'end': end_date.strftime('%Y-%m-%d')
    }
    response = requests.get(url, params=params)
    data = response.json()
    df_water_level = pd.DataFrame(data)
    df_water_level['date'] = pd.to_datetime(df_water_level['date'])
    return df_water_level

# Шаг 2: Сбор данных о ценах криптовалюты
def fetch_crypto_price_data(symbol, start_date, end_date):
    # Используем API CoinGecko для получения исторических данных о ценах BTC
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range"
    params = {
        'vs_currency': 'usd',
        'from': int(start_date.timestamp()),
        'to': int(end_date.timestamp())
    }
    response = requests.get(url, params=params)
    data = response.json()
    df_crypto_price = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df_crypto_price['date'] = pd.to_datetime(df_crypto_price['timestamp'], unit='ms')
    return df_crypto_price

# Шаг 3: Анализ корреляции
def analyze_correlation(df_water_level, df_crypto_price):
    # Объединение данных по дате
    merged_df = pd.merge_asof(df_water_level.sort_values('date'), 
                              df_crypto_price.sort_values('date'), 
                              on='date')
    correlation = merged_df['level'].corr(merged_df['price'])
    print(f"Корреляция между уровнем воды и ценой криптовалюты: {correlation}")
    return merged_df

# Шаг 4: Разработка стратегии торговли
def trading_strategy(df):
    # Простая стратегия: покупаем, если уровень воды выше среднего, продаем ниже
    df['signal'] = np.where(df['level'] > df['level'].mean(), 1, -1)
    df['returns'] = df['price'].pct_change()
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']
    return df

# Шаг 5: Симуляция торговли
def simulate_trading(df):
    initial_capital = 10000
    df['capital'] = initial_capital * (1 + df['strategy_returns']).cumprod()
    print(f"Итоговый капитал после торговли: {df['capital'].iloc[-1]}")
    return df

# Шаг 6: Визуализация результатов
def visualize_results(df):
    # Предположим, что у нас есть координаты реки Аягоз
    aigaz_coords = [52.3740300, 104.2938900]
    
    m = folium.Map(location=aigaz_coords, zoom_start=10)
    
    # Добавление маркера с информацией о торговле
    folium.Marker(
        location=aigaz_coords,
        popup=f"Итоговый капитал: {df['capital'].iloc[-1]:.2f} USD",
        icon=folium.Icon(color='blue')
    ).add_to(m)
    
    m.save("236.html")

# Основной код
if __name__ == "__main__":
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    
    df_water_level = fetch_water_level_data(start_date, end_date)
    df_crypto_price = fetch_crypto_price_data('bitcoin', start_date, end_date)
    
    merged_df = analyze_correlation(df_water_level, df_crypto_price)
    strategy_df = trading_strategy(merged_df)
    result_df = simulate_trading(strategy_df)
    
    visualize_results(result_df)