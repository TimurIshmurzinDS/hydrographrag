import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

# 1. Симуляция данных (так как реальные данные требуют доступа к закрытым БД гидромета)
# Создаем временной ряд за последние 10 лет (ежедневные замеры)
np.random.seed(42)
date_rng = pd.date_range(start='2014-01-01', end='2023-12-31', freq='D')
# Базовый уровень + сезонность (синусоида) + случайный шум + один экстремальный пик (паводок)
base_level = 1.5
seasonality = 0.5 * np.sin(2 * np.pi * date_rng.dayofyear / 365)
noise = np.random.normal(0, 0.2, len(date_rng))
water_levels = base_level + seasonality + noise

# Добавляем аномальный пиковый уровень (например, сильный паводок в 2021 году)
peak_index = 2500 
water_levels[peak_index] = 4.8  # Пиковый уровень в метрах

df = pd.DataFrame({'date': date_rng, 'level': water_levels})

# 2. Расчет показателей
peak_level = df['level'].max()
average_level = df['level'].mean()
difference = peak_level - average_level
percentage_increase = (difference / average_level) * 100

print(f"Пиковый уровень воды: {peak_level:.2f} м")
print(f"Средний многолетний показатель: {average_level:.2f} м")
print(f"Разница: {difference:.2f} м ({percentage_increase:.1f}%)")

# 3. Геопространственная визуализация
# Координаты реки Малая Алматинка (примерная точка в черте города/предгорья)
coords_kishi_almaty = [43.2385, 76.9210]

# Создание карты
m = folium.Map(location=coords_kishi_almaty, zoom_start=12, tiles='OpenStreetMap')

# Текст для всплывающего окна
popup_text = (
    f"<b>Река Малая Алматинка (Kishi Almaty River)</b><br>"
    f"Пиковый уровень: {peak_level:.2f} м<br>"
    f"Средний уровень: {average_level:.2f} м<br>"
    f"Отклонение: +{difference:.2f} м ({percentage_increase:.1f}%)"
)

# Добавление маркера гидропоста
folium.Marker(
    location=coords_kishi_almaty,
    popup=folium.Popup(popup_text, max_width=300),
    tooltip="Гидропост Малая Алматинка",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление линии, имитирующей русло реки (упрощенно)
river_path = [
    [43.2600, 76.9000], 
    [43.2450, 76.9100], 
    [43.2385, 76.9210], 
    [43.2200, 76.9300]
]
folium.PolyLine(river_path, color="blue", weight=4, opacity=0.8, tooltip="Kishi Almaty River").add_to(m)

# Сохранение карты
m.save("122.html")
print("Карта успешно сохранена в файл 122.html")