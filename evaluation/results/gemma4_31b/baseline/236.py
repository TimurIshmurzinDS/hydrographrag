import pandas as pd
import numpy as np
import folium
import random
from datetime import datetime

class AyagozCryptoBot:
    def __init__(self, symbol="BTC/USDT"):
        self.symbol = symbol
        self.balance_usd = 10000.0
        self.balance_crypto = 0.0
        # Координаты реки Аягоз (примерные координаты региона)
        self.coords = [48.0, 78.0] 
        self.water_level_threshold_high = 5.5  # Метры
        self.water_level_threshold_low = 3.0   # Метры

    def get_river_level(self):
        """
        Симуляция получения данных с гидрологического поста.
        В реальном сценарии здесь был бы запрос к API гидромета.
        """
        return round(random.uniform(2.0, 7.0), 2)

    def execute_trade(self, signal, current_price):
        """
        Логика исполнения сделок.
        """
        if signal == "BUY" and self.balance_usd > 0:
            amount_to_buy = self.balance_usd / current_price
            self.balance_crypto += amount_to_buy
            self.balance_usd = 0
            print(f"[{datetime.now()}] SIGNAL: BUY | Action: Bought {amount_to_buy:.4f} {self.symbol}")
        
        elif signal == "SELL" and self.balance_crypto > 0:
            amount_to_sell = self.balance_crypto * current_price
            self.balance_usd += amount_to_sell
            self.balance_crypto = 0
            print(f"[{datetime.now()}] SIGNAL: SELL | Action: Sold all {self.symbol} for ${amount_to_sell:.2f}")
        
        else:
            print(f"[{datetime.now()}] SIGNAL: HOLD | No action taken.")

    def run_strategy(self, current_crypto_price):
        """
        Основной цикл стратегии: Уровень реки -> Сигнал -> Сделка.
        """
        level = self.get_river_level()
        print(f"Current Ayagoz River Level: {level}m")

        if level > self.water_level_threshold_high:
            signal = "BUY"
        elif level < self.water_level_threshold_low:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        self.execute_trade(signal, current_crypto_price)
        return level, signal

# --- Main Execution ---

# Инициализация бота
bot = AyagozCryptoBot()
mock_crypto_price = 65000.0  # Текущая цена BTC

# Запуск одной итерации алгоритма
current_level, current_signal = bot.run_strategy(mock_crypto_price)

# --- GIS Visualization ---

# Создание карты вокруг реки Аягоз
m = folium.Map(location=bot.coords, zoom_start=8, tiles="OpenStreetMap")

# Определение цвета маркера в зависимости от сигнала
color = "green" if current_signal == "BUY" else "red" if current_signal == "SELL" else "blue"

# Добавление маркера станции мониторинга
folium.Marker(
    location=bot.coords,
    popup=f"Ayagoz River Station\nLevel: {current_level}m\nSignal: {current_signal}",
    tooltip="Hydro-Crypto Sensor",
    icon=folium.Icon(color=color, icon="info-sign")
).add_to(m)

# Сохранение карты
m.save("236.html")

print("\nModeling complete. The map has been saved as '236.html'.")
print(f"Final Portfolio: USD: {bot.balance_usd:.2f}, Crypto: {bot.balance_crypto:.4f}")