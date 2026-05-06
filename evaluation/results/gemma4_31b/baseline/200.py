import pandas as pd
import numpy as np
import folium
from folium.plugins import PolyLineText

# 1. Симуляция исторических данных (так как реальные данные реки Kishi Osek специфичны)
# Создаем датасет: Год и Максимальный уровень воды в метрах
np.random.seed(42)
years = np.arange(1980, 2024)
# Генерируем нормальные значения с добавлением нескольких случайных экстремумов
water_levels = np.random.normal(loc=2.5, scale=0.5, size=len(years))
# Искусственно создаем экстремальные паводки в определенные годы
extreme_years_indices = [5, 15, 30, 42] # Индексы лет с паводками
for idx in extreme_years_indices:
    water_levels[idx] = np.random.uniform(4.5, 6.0)

df = pd.DataFrame({'Year': years, 'WaterLevel': water_levels})

# 2. Статистический анализ для выявления экстремумов
mean_level = df['WaterLevel'].mean()
std_level = df['WaterLevel'].std()
threshold = mean_level + 2 * std_level  # Порог экстремума (Среднее + 2 сигмы)

# Выявление экстремальных лет
extreme_floods = df[df['WaterLevel'] > threshold].copy()
extreme_floods['Deviation'] = extreme_floods['WaterLevel'] - mean_level

print(f"Средний уровень: {mean_level:.2f} м")
print(f"Порог экстремального паводка: {threshold:.2f} м")
print("\nГоды экстремальных паводков:")
print(extreme_floods[['Year', 'WaterLevel']])

# 3. Геопространственная визуализация
# Координаты реки Kishi Osek (приблизительные координаты для региона Центральной Азии)
# В реальном проекте здесь используется GeoJSON файл русла реки
river_coords = [
    [39.50, 72.10], [39.52, 72.15], [39.55, 72.20], 
    [39.58, 72.25], [39.62, 72.30], [39.65, 72.35]
]

# Создание карты
m = folium.Map(location=[39.57, 72.22], zoom_start=11, tiles='OpenStreetMap')

# Отрисовка русла реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Kishi Osek River").add_to(m)

# Добавление маркеров гидропостов (симуляция)
stations = [
    {"name": "Station Alpha (Upper)", "loc": [39.50, 72.10], "status": "Normal"},
    {"name": "Station Beta (Middle)", "loc": [39.58, 72.25], "status": "Critical"},
    {"name": "Station Gamma (Lower)", "loc": [39.65, 72.35], "status": "Normal"},
]

for station in stations:
    color = 'red' if station['status'] == 'Critical' else 'green'
    folium.CircleMarker(
        location=station['loc'],
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"{station['name']} - Status: {station['status']}"
    ).add_to(m)

# Добавление текстовой информации о найденных экстремумах на карту
extreme_years_str = ", ".join(extreme_floods['Year'].astype(str).tolist())
info_text = f"Extreme Flood Years identified: {extreme_years_str}"
folium.Marker(
    location=[39.57, 72.22],
    icon=folium.DivIcon(html=f'<div style="font-family: Arial; color: white; background: rgba(0,0,0,0.6); padding: 10px; border-radius: 5px; width: 300px;"><b>Analysis Result:</b><br>{info_text}</div>')
).add_to(m)

# Сохранение карты
m.save("200.html")
print("\nMap has been saved as 200.html")