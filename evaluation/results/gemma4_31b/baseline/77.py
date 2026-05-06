import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta

# 1. Генерация синтетических данных для рек Баскан и Проходная
def generate_river_data(river_name, base_flow, peak_flow, peak_month, noise_level=0.1):
    np.random.seed(42 if river_name == "Baskan" else 7)
    dates = pd.date_range(start="2022-01-01", end="2023-12-31", freq='D')
    
    # Создаем сезонную синусоиду, смещенную к весне (март-апрель)
    # peak_month: 3 = March, 4 = April
    day_of_year = dates.dayofyear
    # Смещение фазы так, чтобы пик был в указанный месяц
    phase_shift = 31 * (peak_month - 1) 
    
    # Модель расхода: Базовый уровень + Амплитуда * sin(сезон)
    seasonal_pattern = (peak_flow - base_flow) * (
        1 + np.sin(2 * np.pi * (day_of_year - phase_shift) / 365)
    ) / 2
    
    flow = base_flow + seasonal_pattern + np.random.normal(0, noise_flow := base_flow * noise_level, len(dates))
    flow = np.maximum(flow, 0.1) # Расход не может быть отрицательным
    
    return pd.DataFrame({'Date': dates, 'River': river_name, 'Discharge': flow})

# Параметры: Баскан (крупнее), Проходная (меньше, более резкий пик)
df_baskan = generate_river_data("Baskan", base_flow=0.5, peak_flow=4.2, peak_month=4)
df_prokhodnaya = generate_river_data("Prokhodnaya", base_flow=0.2, peak_flow=2.8, peak_month=3)

df = pd.concat([df_baskan, df_prokhodnaya])

# 2. Анализ весеннего половодья (Март - Май)
def analyze_flood(df_river):
    spring_data = df_river[(df_river['Date'].dt.month >= 3) & (df_river['Date'].dt.month <= 5)]
    max_flow = spring_data['Discharge'].max()
    avg_flow = spring_data['Discharge'].mean()
    peak_date = spring_data.loc[spring_data['Discharge'].idxmax(), 'Date']
    return max_flow, avg_flow, peak_date

b_max, b_avg, b_date = analyze_flood(df_baskan)
p_max, p_avg, p_date = analyze_flood(df_prokhodnaya)

print(f"Baskan River: Max Flow = {b_max:.2f} m3/s, Peak Date = {b_date.date()}")
print(f"Prokhodnaya River: Max Flow = {p_max:.2f} m3/s, Peak Date = {p_date.date()}")

# 3. Визуализация графиков расхода
plt.figure(figsize=(12, 6))
plt.plot(df_baskan['Date'], df_baskan['Discharge'], label='Baskan River', color='blue')
plt.plot(df_prokhodnaya['Date'], df_prokhodnaya['Discharge'], label='Prokhodnaya River', color='green')
plt.title("Seasonal River Discharge Comparison")
plt.xlabel("Date")
plt.ylabel("Discharge (m3/s)")
plt.legend()
plt.grid(True)
plt.savefig("discharge_plot.png")
plt.show()

# 4. Геопространственная визуализация (Folium)
# Координаты (приблизительные для региона Крыма)
locations = {
    "Baskan": [45.15, 34.20, b_max],
    "Prokhodnaya": [45.05, 34.10, p_max]
}

# Создание карты
m = folium.Map(location=[45.1, 34.15], zoom_start=9, tiles='OpenStreetMap')

for river, data in locations.items():
    lat, lon, flow = data
    # Определяем цвет в зависимости от интенсивности потока (условно)
    color = 'red' if flow > 3.0 else 'orange' if flow > 2.0 else 'green'
    
    folium.Marker(
        location=[lat, lon],
        popup=f"River: {river}<br>Max Spring Flow: {flow:.2f} m3/s",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)
    
    # Добавляем линию, имитирующую русло реки (упрощенно)
    if river == "Baskan":
        coords = [[45.15, 34.20], [45.20, 34.30], [45.25, 34.40]]
    else:
        coords = [[45.05, 34.10], [45.08, 34.15]]
    
    folium.PolyLine(coords, color=color, weight=4, opacity=0.8, popup=river).add_to(m)

# Сохранение карты
m.save("77.html")

print("Modeling complete. Map saved as 77.html and plot saved as discharge_plot.png")