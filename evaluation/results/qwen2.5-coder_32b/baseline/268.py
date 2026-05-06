import pandas as pd
import numpy as np
import requests
from folium import Map, Marker, Popup, Icon
import matplotlib.pyplot as plt

# Шаг 1: Сбор данных о криптовалютах
def fetch_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

# Шаг 2: Анализ данных
def analyze_crypto_data(df):
    # Выбираем топ-5 криптовалют по капитализации
    top_cryptos = df.head(5)
    return top_cryptos

# Шаг 3: Моделирование рисков (простая модель на основе волатильности)
def risk_modeling(df):
    # Пример простой модели, которая оценивает риск как стандартное отклонение цены
    df['price_change_percentage_24h'] = pd.to_numeric(df['price_change_percentage_24h'], errors='coerce')
    df['risk_score'] = np.abs(df['price_change_percentage_24h'])
    return df

# Шаг 4: Выбор оптимальной криптовалюты
def select_optimal_crypto(df):
    # Выбираем криптовалюту с наименьшим риском (минимальное стандартное отклонение цены)
    optimal_crypto = df.loc[df['risk_score'].idxmin()]
    return optimal_crypto

# Шаг 5: Визуализация результатов
def visualize_results(optimal_crypto):
    # Координаты реки Бутак (примерные, так как точные координаты не указаны)
    butak_coords = [43.2067, 131.8958]
    
    m = Map(location=butak_coords, zoom_start=10)
    
    # Добавляем маркер для реки Бутак
    Marker(
        location=butak_coords,
        popup=f"Река Бутак\nВыбранная криптовалюта: {optimal_crypto['name']}",
        icon=Icon(color='green')
    ).add_to(m)
    
    # Сохраняем карту в HTML файл
    m.save("268.html")

# Основной код
if __name__ == "__main__":
    crypto_data = fetch_crypto_data()
    top_cryptos = analyze_crypto_data(crypto_data)
    risky_cryptos = risk_modeling(top_cryptos)
    optimal_crypto = select_optimal_crypto(risky_cryptos)
    visualize_results(optimal_crypto)

    # Выводим информацию о выбранной криптовалюте
    print(f"Оптимальная криптовалюта для инвестиций: {optimal_crypto['name']}")