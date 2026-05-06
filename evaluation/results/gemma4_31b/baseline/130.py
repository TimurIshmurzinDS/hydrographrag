import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta

# 1. Симуляция исторических данных (так как реальные данные закрыты или требуют API)
np.random.seed(42)
dates = pd.date_range(start="2010-01-01", end="2023-12-31", freq='M')
n = len(dates)

# Генерация стока для Shilik River (Базовый уровень)
# Добавляем сезонность (синусоида) + шум
shilik_flow = 15 + 10 * np.sin(np.linspace(0, 2 * np.pi * (n/12), n)) + np.random.normal(0, 2, n)
shilik_flow = np.maximum(shilik_flow, 2) # Сток не может быть отрицательным

# Генерация стока для Bayankol River (с определенным отклонением и трендом на снижение)
trend = np.linspace(0, -5, n) 
bayankol_flow = 12 + 8 * np.sin(np.linspace(0, 2 * np.pi * (n/12), n)) + trend + np.random.normal(0, 3, n)
bayankol_flow = np.maximum(bayankol_flow, 1)

df = pd.DataFrame({
    'Date': dates,
    'Shilik_Q': shilik_flow,
    'Bayankol_Q': bayankol_flow
})

# 2. Расчет отклонений
df['Abs_Deviation'] = df['Bayankol_Q'] - df['Shilik_Q']
df['Rel_Deviation_Pct'] = (df['Abs_Deviation'] / df['Shilik_Q']) * 100

# 3. Статистический анализ
mean_dev = df['Abs_Deviation'].mean()
max_dev = df['Abs_Deviation'].max()
min_dev = df['Abs_Deviation'].min()

print(f"Среднее отклонение стока Bayankol от Shilik: {mean_dev:.2f} м3/с")
print(f"Максимальное отклонение: {max_dev:.2f} м3/с")
print(f"Минимальное отклонение: {min_dev:.2f} м3/с")

# 4. Визуализация временных рядов
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Shilik_Q'], label='Shilik River (Baseline)', color='blue', linewidth=2)
plt.plot(df['Date'], df['Bayankol_Q'], label='Bayankol River', color='green', linewidth=2)
plt.fill_between(df['Date'], df['Shilik_Q'], df['Bayankol_Q'], color='gray', alpha=0.3, label='Deviation Area')
plt.title('Historical Discharge Comparison: Bayankol vs Shilik')
plt.xlabel('Year')
plt.ylabel('Discharge (m3/s)')
plt.legend()
plt.grid(True)
plt.savefig("discharge_analysis.png")
plt.close()

# 5. Геопространственная визуализация (Folium)
# Приблизительные координаты рек в регионе Казахстана/Центральной Азии
coords_shilik = [[48.5, 78.0], [48.7, 79.0], [49.0, 80.0]] # Условная линия
coords_bayankol = [[47.5, 77.0], [47.8, 78.5], [48.1, 79.5]] # Условная линия

m = folium.Map(location=[48.2, 78.5], zoom_start=6, tiles='CartoDB positron')

# Отрисовка реки Shilik (Базовая)
folium.PolyLine(coords_shilik, color='blue', weight=4, opacity=0.8, 
                tooltip='Shilik River (Baseline)').add_to(m)

# Отрисовка реки Bayankol
folium.PolyLine(coords_bayankol, color='green', weight=4, opacity=0.8, 
                tooltip='Bayankol River').add_to(m)

# Добавление маркеров гидропостов с данными об отклонении
folium.CircleMarker(
    location=[49.0, 80.0],
    radius=8,
    popup=f"Shilik Station: Baseline Level",
    color='blue',
    fill=True,
    fill_color='blue'
).add_to(m)

folium.CircleMarker(
    location=[48.1, 79.5],
    radius=8,
    popup=f"Bayankol Station: Avg Deviation {mean_dev:.2f} m3/s",
    color='green',
    fill=True,
    fill_color='green'
).add_to(m)

# Сохранение карты
m.save("130.html")

print("Analysis complete. Map saved as 130.html and plot as discharge_analysis.png")