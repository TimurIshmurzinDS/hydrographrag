import folium
import numpy as np
import pandas as pd
import math

def calculate_mining_capacity(flow_rate, head=10, efficiency=0.8):
    """
    Расчет мощности майнинга на основе расхода воды.
    flow_rate: расход воды (м3/с)
    head: напор воды (метры)
    efficiency: КПД установки
    """
    rho = 1000  # плотность воды кг/м3
    g = 9.81    # ускорение свободного падения
    
    # Мощность в Ваттах: P = eta * rho * g * h * Q
    power_watts = efficiency * rho * g * head * flow_rate
    
    # Энергоэффективность ASIC (например, 30 Вт на 1 TH/s)
    watts_per_th = 30 
    hashrate_th = power_watts / watts_per_th
    
    return hashrate_th

# 1. Симуляция сезонного расхода реки Или (средние значения м3/с)
# Месяцы: Янв, Фев, Мар, Апр, Май, Июн, Июл, Авг, Сен, Окт, Ноя, Дек
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
# Моделируем пик в мае-июне (таяние ледников)
seasonal_flow = [150, 160, 250, 400, 700, 850, 600, 400, 250, 200, 170, 150]

# 2. Координаты русла реки Или (упрощенно: от границы до Балхаша)
ili_river_coords = [
    [42.5, 78.0], [42.7, 79.0], [42.8, 80.0], [42.6, 81.0], 
    [42.4, 82.0], [42.2, 83.0], [42.0, 84.0], [41.8, 85.0]
]

# 3. Точки размещения майнинг-ферм (выбираем 3 точки вдоль реки)
farm_locations = [
    {"name": "Farm_North", "coords": [42.7, 79.0], "head": 12},
    {"name": "Farm_Central", "coords": [42.4, 82.0], "head": 8},
    {"name": "Farm_South", "coords": [41.8, 85.0], "head": 5},
]

# Создание карты
m = folium.Map(location=[42.3, 81.5], zoom_start=6, tiles="CartoDB positron")

# Отрисовка реки
folium.PolyLine(ili_river_coords, color="blue", weight=4, opacity=0.7, tooltip="Река Или").add_to(m)

# Добавление ферм на карту
for farm in farm_locations:
    # Рассчитаем средний хешрейт за год для этого места
    avg_hashrate = np.mean([calculate_mining_capacity(q, farm['head']) for q in seasonal_flow])
    
    # Создаем всплывающее окно с сезонной динамикой
    popup_text = f"<b>{farm['name']}</b><br>Средний хешрейт: {avg_hashrate:.2f} TH/s<br><br>"
    for month, flow in zip(months, seasonal_flow):
        hr = calculate_mining_capacity(flow, farm['head'])
        popup_text += f"{month}: {hr:.1f} TH/s<br>"
    
    folium.CircleMarker(
        location=farm['coords'],
        radius=10,
        popup=folium.Popup(popup_text, max_width=300),
        color="orange",
        fill=True,
        fill_color="orange"
    ).add_to(m)

# Сохранение карты
m.save("227.html")

print("Моделирование завершено. Результаты сохранены в файл 227.html")