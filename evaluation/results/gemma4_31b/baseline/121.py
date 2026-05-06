import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime

# 1. Симуляция данных о расходе воды (Water Discharge)
# В реальном сценарии здесь был бы запрос к API гидрологической службы или загрузка CSV
np.random.seed(42)
years = np.arange(2014, 2024)
months = np.arange(1, 13)

# Создаем сетку дат
dates = pd.date_range(start='2014-01-01', end='2023-12-31', freq='M')

# Генерируем синтетические данные: 
# Shilik обычно крупнее, чем Bayankol.
# Добавляем сезонность (синусоида) и случайный шум
def generate_discharge(base_mean, amplitude, noise_level, dates):
    seasonal = amplitude * np.sin(2 * np.pi * dates.month / 12)
    noise = np.random.normal(0, noise_level, len(dates))
    return base_mean + seasonal + noise

shilik_data = generate_discharge(15.0, 8.0, 2.0, dates)
bayankol_data = generate_discharge(5.0, 3.0, 1.0, dates)

df = pd.DataFrame({
    'Date': dates,
    'Shilik_River': shilik_data,
    'Bayankol_River': bayankol_data
})

# 2. Расчет средних значений
avg_shilik = df['Shilik_River'].mean()
avg_bayankol = df['Bayankol_River'].mean()

print(f"Средний расход воды в реке Shilik за 10 лет: {avg_shilik:.2f} м3/с")
print(f"Средний расход воды в реке Bayankol за 10 лет: {avg_bayankol:.2f} м3/с")
print(f"Разница: {avg_shilik - avg_bayankol:.2f} м3/с")

# 3. Визуализация графиков
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Shilik_River'], label='Shilik River', color='blue', alpha=0.7)
plt.plot(df['Date'], df['Bayankol_River'], label='Bayankol River', color='green', alpha=0.7)
plt.title('Динамика расхода воды в реках Shilik и Bayankol (2014-2023)')
plt.xlabel('Год')
plt.ylabel('Расход воды (м3/с)')
plt.legend()
plt.grid(True)
plt.savefig("discharge_comparison.png")
plt.show()

# 4. Геопространственная визуализация (Folium)
# Примерные координаты рек (Центральная Азия/Казахстан)
locations = {
    "Shilik River": [44.5, 81.5, avg_shilik],
    "Bayankol River": [44.2, 82.1, avg_bayankol]
}

# Создаем карту, центрированную между реками
m = folium.Map(location=[44.35, 81.8], zoom_start=7, tiles='OpenStreetMap')

for river, data in locations.items():
    folium.Marker(
        location=[data[0], data[1]],
        popup=f"<b>{river}</b><br>Средний расход (10 лет): {data[2]:.2f} м3/с",
        tooltip=river,
        icon=folium.Icon(color='blue' if 'Shilik' in river else 'green', icon='info-sign')
    ).add_to(m)

# Сохранение карты строго в файл 121.html
m.save("121.html")

print("Анализ завершен. Карта сохранена в файл 121.html")