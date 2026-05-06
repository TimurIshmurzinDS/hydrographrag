import pandas as pd
import numpy as np
import folium

# Предположим, что у нас есть данные о расходе воды для рек Tekes River и Bayankol River.
# Для примера создадим синтетические временные ряды данных.

# Создание синтетических данных
np.random.seed(0)
dates = pd.date_range(start='2018-01-01', end='2023-12-31')
tekes_data = np.random.normal(loc=50, scale=10, size=len(dates))
bayankol_data = np.random.normal(loc=40, scale=8, size=len(dates))

# Создание DataFrame
df_tekes = pd.DataFrame({'Date': dates, 'Discharge': tekas_data})
df_bayankol = pd.DataFrame({'Date': dates, 'Discharge': bayankol_data})

# Установка даты как индекса
df_tekes.set_index('Date', inplace=True)
df_bayankol.set_index('Date', inplace=True)

# Расчет среднего значения за последние 5 лет для каждой реки
mean_tekes = df_tekes['Discharge'].mean()
mean_bayankol = df_bayankol['Discharge'].mean()

# Нахождение максимального увеличения расхода воды по сравнению со средним значением
max_increase_tekes = (df_tekes['Discharge'] - mean_tekes).max()
max_increase_bayankol = (df_bayankol['Discharge'] - mean_bayankol).max()

# Сравнение результатов
if max_increase_tekes > max_increase_bayankol:
    result = "Tekes River"
else:
    result = "Bayankol River"

print(f"Река с наибольшим увеличением расхода воды: {result}")

# Координаты рек (примерные)
tekes_coords = [42.8536, 79.1016]  # примерные координаты Tekes River
bayankol_coords = [43.2629, 80.5764]  # примерные координаты Bayankol River

# Создание карты с помощью folium
m = folium.Map(location=[43.0, 80.0], zoom_start=8)

# Добавление маркеров для рек
folium.Marker(tekes_coords, popup=f'Tekes River\nMax Increase: {max_increase_tekes:.2f}').add_to(m)
folium.Marker(bayankol_coords, popup=f'Bayankol River\nMax Increase: {max_increase_bayankol:.2f}').add_to(m)

# Добавление маркера для реки с наибольшим увеличением расхода воды
if result == "Tekes River":
    folium.Marker(tekes_coords, popup=f'Tekes River\nMax Increase: {max_increase_tekes:.2f}', icon=folium.Icon(color='red')).add_to(m)
else:
    folium.Marker(bayankol_coords, popup=f'Bayankol River\nMax Increase: {max_increase_bayankol:.2f}', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("125.html")