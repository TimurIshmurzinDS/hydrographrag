import folium
import numpy as np
import pandas as pd

def simulate_btc_impact(water_level_drop_percent):
    """
    Симуляция влияния уровня воды в р. Эмел на курс Биткоина.
    water_level_drop_percent: процент падения уровня воды (0-100)
    """
    # Константы
    current_btc_price = 65000  # USD
    global_hashrate_share = 0.02  # Допустим, регион Эмел дает 2% глобального хешрейта
    
    # 1. Зависимость выработки энергии от уровня воды (нелинейная)
    # Если уровень падает более чем на 30%, энергоснабжение падает резко
    energy_availability = np.exp(-water_level_drop_percent / 50) 
    
    # 2. Влияние на локальный хешрейт
    # Потеря мощностей пропорциональна потере энергии
    hashrate_loss = global_hashrate_share * (1 - energy_availability)
    
    # 3. Влияние на цену (упрощенная модель)
    # Падение хешрейта может вызвать панику или, наоборот, перераспределение.
    # Предположим, что падение хешрейта на 1% вызывает колебание цены на 0.5%
    price_change_percent = hashrate_loss * 100 * -0.5 
    new_price = current_btc_price * (1 + price_change_percent / 100)
    
    return new_price, hashrate_loss

# Параметры сценария
drop_percent = 40  # Сценарий: уровень воды упал на 40%
final_price, loss = simulate_btc_impact(drop_percent)

print(f"Сценарий: Падение уровня воды в р. Эмел на {drop_percent}%")
print(f"Потеря глобального хешрейта: {loss:.4%}")
print(f"Прогнозируемый курс BTC: ${final_price:.2f}")

# --- Визуализация на карте ---

# Координаты реки Эмел (приблизительный центр)
emel_coords = [43.5, 78.5] 

# Создание карты
m = folium.Map(location=emel_coords, zoom_start=6, tiles="CartoDB positron")

# Отрисовка реки (упрощенно линией)
river_points = [
    [43.2, 77.5], [43.4, 78.0], [43.6, 78.5], [43.8, 79.0]
]
folium.PolyLine(river_points, color="blue", weight=5, opacity=0.7, tooltip="Река Эмел").add_to(m)

# Добавление гипотетических майнинг-центров в зоне риска
mining_centers = [
    {"name": "Mining Hub Alpha", "loc": [43.4, 78.1], "risk": "High"},
    {"name": "Mining Hub Beta", "loc": [43.7, 78.6], "risk": "Medium"},
    {"name": "Energy Station Gamma", "loc": [43.5, 78.4], "risk": "Critical"},
]

for center in mining_centers:
    color = "red" if center["risk"] == "Critical" else "orange" if center["risk"] == "High" else "yellow"
    folium.CircleMarker(
        location=center["loc"],
        radius=10,
        popup=f"{center['name']} - Risk: {center['risk']}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Добавление информационного окна
info_text = f"Анализ засухи р. Эмел<br>Падение уровня: {drop_percent}%<br>Прогноз BTC: ${final_price:.2f}"
folium.Popup(info_text).add_to(m)

# Сохранение карты
m.save("258.html")
print("Карта сохранена в файл 258.html")