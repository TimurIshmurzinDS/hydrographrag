import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 1. Эмуляция данных (так как доступ к закрытым гидропостам ограничен)
# В реальном сценарии здесь был бы запрос к API гидрологической службы или чтение CSV/NetCDF
def generate_spring_discharge_data():
    """Генерирует синтетические данные расхода воды для весеннего периода"""
    dates = pd.date_range(start="2023-03-01", end="2023-05-31", freq='D')
    
    # Моделируем кривую половодья: постепенный рост -> пик в апреле -> спад
    # Базовый расход + синусоидальный всплеск + шум
    base_flow = 2.0
    peak_flow = 15.0
    days = np.arange(len(dates))
    
    # Создаем колоколообразную кривую для имитации таяния снега
    melt_curve = peak_flow * np.exp(-(days - 35)**2 / (2 * 10**2)) 
    noise = np.random.normal(0, 0.5, len(dates))
    
    discharge = base_flow + melt_curve + noise
    return pd.DataFrame({'date': dates, 'discharge_m3s': discharge})

# 2. Анализ данных
df = generate_spring_discharge_data()

# Поиск пикового значения
max_q = df['discharge_m3s'].max()
max_date = df.loc[df['discharge_m3s'].idxmax(), 'date']
avg_q = df['discharge_m3s'].mean()

print(f"Анализ расхода воды в реке Batareyka:")
print(f"Пиковый расход: {max_q:.2f} м3/с (Дата: {max_date.date()})")
print(f"Средний расход за период таяния: {avg_q:.2f} м3/с")

# 3. Визуализация гидрографа
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['discharge_m3s'], color='blue', linewidth=2, label='Расход воды (Q)')
plt.axvline(max_date, color='red', linestyle='--', label=f'Пик: {max_date.date()}')
plt.title('Гидрограф весеннего половодья реки Batareyka')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м3/с)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig("hydrograph.png")
plt.close()

# 4. Геопространственная визуализация (Folium)
# Координаты реки Batareyka (примерные координаты для демонстрации)
river_coords = [55.1234, 60.5678] 

m = folium.Map(location=river_coords, zoom_start=12, tiles='OpenStreetMap')

# Добавление маркера гидрологического поста
folium.Marker(
    location=river_coords,
    popup=f"Гидропост Batareyka\nПиковый расход: {max_q:.2f} м3/с",
    tooltip="Точка замера расхода воды",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление имитации русла реки (линия)
river_line = [
    [55.10, 60.50],
    [55.12, 60.55],
    [55.15, 60.60],
    [55.18, 60.65]
]
folium.PolyLine(river_line, color="blue", weight=5, opacity=0.8, tooltip="Русло реки Batareyka").add_to(m)

# Сохранение карты
m.save("27.html")

print("\nРезультаты успешно сохранены: '27.html' (карта) и 'hydrograph.png' (график).")