import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta

# 1. Симуляция данных (так как реальные данные гидропостов требуют API доступа)
# Создаем временной ряд для периода паводка (март - июль)
dates = pd.date_range(start="2023-03-01", end="2023-07-01", freq='D')
np.random.seed(42)

# Моделируем расход воды: базовый уровень + синусоидальный пик паводка + шум
def generate_discharge(base, peak, noise_level):
    # Создаем кривую паводка (пик в мае)
    t = np.linspace(0, 2 * np.pi, len(dates))
    seasonal_pattern = peak * np.exp(-(t - np.pi)**2 / 2) 
    noise = np.random.normal(0, noise_level, len(dates))
    return base + seasonal_pattern + noise

# Tekes River: более крупная река
tekes_discharge = generate_discharge(base=15, peak=45, noise_level=3)
# Bayankol River: более малая река
bayankol_discharge = generate_discharge(base=5, peak=20, noise_level=2)

df = pd.DataFrame({
    'Date': dates,
    'Tekes_River': tekes_discharge,
    'Bayankol_River': bayankol_discharge
})

# 2. Анализ данных
avg_tekes = df['Tekes_River'].mean()
avg_bayankol = df['Bayankol_River'].mean()
max_tekes = df['Tekes_River'].max()
max_bayankol = df['Bayankol_River'].max()

print(f"Средний расход Tekes: {avg_tekes:.2f} м3/с (Пик: {max_tekes:.2f})")
print(f"Средний расход Bayankol: {avg_bayankol:.2f} м3/с (Пик: {max_bayankol:.2f})")
print(f"Разница в среднем расходе: {avg_tekes / avg_bayankol:.2f} раза")

# 3. Построение графика сравнения
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Tekes_River'], label='Tekes River', color='blue', linewidth=2)
plt.plot(df['Date'], df['Bayankol_River'], label='Bayankol River', color='green', linewidth=2)
plt.title('Сравнение расхода воды в период паводка')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м3/с)')
plt.legend()
plt.grid(True)
plt.savefig("discharge_comparison.png")
plt.close()

# 4. Геопространственная визуализация
# Приблизительные координаты рек (Центральная Азия)
locations = {
    "Tekes River": [45.5, 82.0, avg_tekes],
    "Bayankol River": [44.0, 81.0, avg_bayankol]
}

# Создание карты
m = folium.Map(location=[44.7, 81.5], zoom_start=6, tiles='OpenStreetMap')

for river, data in locations.items():
    folium.Marker(
        location=[data[0], data[1]],
        popup=f"<b>{river}</b><br>Средний расход в паводок: {data[2]:.2f} м3/с",
        tooltip=river,
        icon=folium.Icon(color='blue' if 'Tekes' in river else 'green', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("25.html")

print("Результаты успешно сохранены: график 'discharge_comparison.png' и карта '25.html'")