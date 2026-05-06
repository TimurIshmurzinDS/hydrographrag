import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime

# 1. Симуляция данных (так как реальные данные гидропостов требуют доступа к БД)
def generate_river_data(river_name, base_flow, peak_flow, peak_month, noise_level=2):
    """Генерирует синтетический годовой гидрограф реки"""
    months = np.arange(1, 13)
    # Создаем синусоидальную кривую для имитации сезонности
    # Пик смещается в зависимости от peak_month
    seasonal_pattern = np.sin((months - peak_month + 3) * np.pi / 6) 
    # Нормализуем и масштабируем от base_flow до peak_flow
    flow = base_flow + (peak_flow - base_flow) * (seasonal_pattern + 1) / 2
    # Добавляем случайный шум
    noise = np.random.normal(0, noise_level, 12)
    return np.maximum(flow + noise, 0.1)

# Параметры для рек (условно: Турген более полноводная и имеет более выраженный пик)
rivers_params = {
    "Temirlik River": {"base": 2.0, "peak": 15.0, "month": 5},
    "Turgen River": {"base": 5.0, "peak": 45.0, "month": 6}
}

data = {}
for river, params in rivers_params.items():
    data[river] = generate_river_data(river, params['base'], params['peak'], params['month'])

df = pd.DataFrame(data, index=[f"Month_{i}" for i in range(1, 13)])
df.index = pd.to_datetime([f"2023-{i:02d}-01" for i in range(1, 13)])

# 2. Анализ и расчеты
critical_threshold = 30.0  # Порог опасности в м3/с
results = {}

for river in rivers_params.keys():
    peak_val = df[river].max()
    avg_val = df[river].mean()
    risk_level = "High" if peak_val > critical_threshold else "Low"
    results[river] = {"Peak": peak_val, "Avg": avg_val, "Risk": risk_level}

# 3. Визуализация динамики (График)
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Temirlik River"], marker='o', label="Temirlik River", color='blue')
plt.plot(df.index, df["Turgen River"], marker='s', label="Turgen River", color='green')
plt.axhline(y=critical_threshold, color='r', linestyle='--', label="Critical Threshold")
plt.title("Seasonal Water Discharge Comparison")
plt.xlabel("Month")
plt.ylabel("Discharge (m3/s)")
plt.legend()
plt.grid(True)
plt.savefig("discharge_analysis.png")
plt.close()

# 4. Геопространственная визуализация (Folium)
# Координаты (приблизительные для региона Алматы/Турген)
locations = {
    "Temirlik River": [43.15, 77.50],
    "Turgen River": [43.20, 77.80]
}

m = folium.Map(location=[43.17, 77.65], zoom_start=10, tiles="OpenStreetMap")

for river, coords in locations.items():
    risk = results[river]["Risk"]
    color = "red" if risk == "High" else "blue"
    
    # Добавляем маркер станции мониторинга
    folium.CircleMarker(
        location=coords,
        radius=8,
        popup=f"River: {river}<br>Peak Flow: {results[river]['Peak']:.2f} m3/s<br>Risk: {risk}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)
    
    # Добавляем текстовую метку
    folium.Marker(
        location=coords,
        icon=folium.DivIcon(html=f'<div style="font-family: Arial; color: black; font-weight: bold;">{river}</div>')
    ).add_to(m)

# Сохранение карты
m.save("83.html")

print("Analysis complete. Map saved as 83.html. Plot saved as discharge_analysis.png.")
print("\nSummary Table:")
print(pd.DataFrame(results).T)