import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime

# 1. Генерация синтетических данных (имитация гидрологических показателей)
np.random.seed(42)
dates = pd.date_range(start="2014-01-01", end="2023-12-31", freq='M')
n_months = len(dates)

def generate_river_flow(base_flow, amplitude, phase_shift):
    """Генерирует сезонный расход воды с шумом"""
    # Синусоида для имитации сезонности (пик весной/летом)
    time = np.arange(n_months)
    seasonal = amplitude * np.sin(2 * np.pi * time / 12 + phase_shift)
    noise = np.random.normal(0, amplitude * 0.2, n_months)
    return np.maximum(0, base_flow + seasonal + noise)

# Коксу: более стабильный поток, пик в мае
koksu_flow = generate_river_flow(base_flow=15, amplitude=10, phase_shift=np.pi/3)
# Эмель: более выраженная сезонность, пик в апреле
emel_flow = generate_river_flow(base_flow=10, amplitude=12, phase_shift=np.pi/2)

df = pd.DataFrame({
    'Date': dates,
    'Koksu_River': koksu_flow,
    'Emel_River': emel_flow
})
df.set_index('Date', inplace=True)

# 2. Анализ сезонных закономерностей
# Группировка по месяцам для получения среднего профиля за 10 лет
df['Month'] = df.index.month
seasonal_profile = df.groupby('Month')[['Koksu_River', 'Emel_River']].mean()

# 3. Визуализация графиков
plt.figure(figsize=(14, 7))

# График 1: Временные ряды
plt.subplot(2, 1, 1)
plt.plot(df.index, df['Koksu_River'], label='Koksu River', color='blue', alpha=0.7)
plt.plot(df.index, df['Emel_River'], label='Emel River', color='green', alpha=0.7)
plt.title('Historical Water Discharge (2014-2023)')
plt.ylabel('Discharge (m³/s)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# График 2: Сезонный профиль
plt.subplot(2, 1, 2)
plt.plot(seasonal_profile.index, seasonal_profile['Koksu_River'], marker='o', label='Koksu (Avg)', color='blue', linewidth=2)
plt.plot(seasonal_profile.index, seasonal_profile['Emel_River'], marker='s', label='Emel (Avg)', color='green', linewidth=2)
plt.title('Average Seasonal Water Discharge Pattern')
plt.xlabel('Month')
plt.ylabel('Avg Discharge (m³/s)')
plt.xticks(range(1, 13))
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("discharge_analysis.png")
plt.show()

# 4. Геопространственная визуализация
# Примерные координаты рек (для демонстрации)
rivers_coords = {
    "Koksu River": [43.5, 78.5], # Условный центр бассейна
    "Emel River": [43.2, 81.0]   # Условный центр бассейна
}

# Создание карты
m = folium.Map(location=[43.5, 79.5], zoom_start=6, tiles='OpenStreetMap')

# Добавление маркеров рек
for river, coords in rivers_coords.items():
    folium.Marker(
        location=coords,
        popup=f"{river} Basin",
        icon=folium.Icon(color='blue' if 'Koksu' in river else 'green', icon='info-sign')
    ).add_to(m)

# Добавление линий, имитирующих русла (упрощенно)
folium.PolyLine(
    locations=[[43.8, 77.5], [43.5, 78.5], [43.2, 79.0]], 
    color='blue', weight=3, opacity=0.8, tooltip='Koksu River'
).add_to(m)

folium.PolyLine(
    locations=[[44.0, 80.0], [43.2, 81.0], [42.5, 82.0]], 
    color='green', weight=3, opacity=0.8, tooltip='Emel River'
).add_to(m)

# Сохранение карты
m.save("196.html")

print("Analysis complete. Plots saved as 'discharge_analysis.png' and map saved as '196.html'.")