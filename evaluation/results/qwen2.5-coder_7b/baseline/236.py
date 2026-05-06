import requests
import folium
from datetime import datetime

# Функция для получения текущего уровня реки Аягоз
def get_water_level():
    # Пример API для получения данных о уровне реки
    url = "https://api.example.com/water-level"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['water_level']
    else:
        raise Exception("Failed to get water level")

# Функция для получения текущей цены криптовалюты
def get_crypto_price():
    # Пример API для получения данных о ценах на криптовалюту
    url = "https://api.example.com/crypto-price"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['price']
    else:
        raise Exception("Failed to get crypto price")

# Функция для торговли криптовалютой
def trade_crypto():
    water_level = get_water_level()
    crypto_price = get_crypto_price()
    
    if water_level > 100:  # Порог уровня реки
        print(f"Уровень реки {water_level} м. Купим криптовалюту по цене {crypto_price}")
        # Здесь можно добавить код для покупки криптовалюты
    else:
        print(f"Уровень реки {water_level} м. Продадим криптовалюту по цене {crypto_price}")
        # Здесь можно добавить код для продажи криптовалюты

# Функция для визуализации уровня реки на карте
def visualize_water_level():
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)
    
    # Добавляем маркер с уровнем реки
    folium.Marker(
        location=[40.7128, -74.0060],
        popup=f"Уровень реки: {get_water_level()} м",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    m.save("236.html")

# Выполнение алгоритма
trade_crypto()
visualize_water_level()