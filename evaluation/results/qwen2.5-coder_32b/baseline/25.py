import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
import folium

# Предполагаемые данные о расходе воды для рек Текес и Байынкөл
data = {
    'date': pd.date_range(start='2023-04-01', periods=60, freq='D'),
    'tekes_discharge': np.random.normal(loc=50, scale=10, size=60),
    'bayankol_discharge': np.random.normal(loc=40, scale=8, size=60)
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование столбца даты в формат datetime
df['date'] = pd.to_datetime(df['date'])

# Определение периода паводка (например, среднее значение + 2 стандартных отклонения)
tekes_mean = df['tekes_discharge'].mean()
tekes_std = df['tekes_discharge'].std()
bayankol_mean = df['bayankol_discharge'].mean()
bayankol_std = df['bayankol_discharge'].std()

# Определение пороговых значений для паводка
tekes_flood_threshold = tekes_mean + 2 * tekes_std
bayankol_flood_threshold = bayankol_mean + 2 * bayankol_std

# Выделение периодов паводка
df['tekes_flood'] = df['tekes_discharge'] > tekes_flood_threshold
df['bayankol_flood'] = df['bayankol_discharge'] > bayankol_flood_threshold

# Построение графиков расхода воды и пороговых значений для паводка
plt.figure(figsize=(14, 7))
plt.plot(df['date'], df['tekes_discharge'], label='Река Текес', color='blue')
plt.axhline(y=tekes_flood_threshold, color='red', linestyle='--', label='Порог паводка для Текес')
plt.fill_between(df['date'], tekes_flood_threshold, df['tekes_discharge'].max(), where=df['tekes_flood'], color='blue', alpha=0.3)
plt.plot(df['date'], df['bayankol_discharge'], label='Река Байынкөл', color='green')
plt.axhline(y=bayankol_flood_threshold, color='orange', linestyle='--', label='Порог паводка для Байынкөл')
plt.fill_between(df['date'], bayankol_flood_threshold, df['bayankol_discharge'].max(), where=df['bayankol_flood'], color='green', alpha=0.3)
plt.xlabel('Дата')
plt.ylabel('Расход воды (куб. м/с)')
plt.title('Сравнение уровней расхода воды рек Текес и Байынкөл в период паводка')
plt.legend()
plt.grid(True)
plt.show()

# Создание интерактивной карты с помощью folium
m = folium.Map(location=[42.8746, 80.9451], zoom_start=10)  # Координаты примерного центра рек

# Добавление маркеров для местоположения рек и уровня их расхода в период паводка
folium.Marker(
    location=[42.8746, 80.9451],  # Координаты Текес
    popup=f"Текес: Порог паводка {tekes_flood_threshold:.2f} куб. м/с",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[43.0517, 86.9617],  # Координаты Байынкөл
    popup=f"Байынкөл: Порог паводка {bayankol_flood_threshold:.2f} куб. м/с",
    icon=folium.Icon(color='green')
).add_to(m)

# Сохранение карты в файл
m.save("25.html")