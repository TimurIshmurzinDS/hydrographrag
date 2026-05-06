import pandas as pd
import folium

# 1. Загрузка данных о расходе воды (замените 'data.csv' на фактический файл)
data = pd.read_csv('data.csv', index_col='Date', parse_dates=True)

# 2. Обработка и подготовка данных (пример интерполяции)
data['Discharge'].interpolate(method='linear', inplace=True)

# 3. Выделение периода паводка (замените даты на фактические)
flood_period = data['2023-04-15':'2023-05-15']

# 4. Анализ изменений расхода воды
avg_discharge = flood_period['Discharge'].mean()
max_discharge = flood_period['Discharge'].max()
min_discharge = flood_period['Discharge'].min()

# 5. Визуализация на карте
m = folium.Map(location=[55.75, 37.62], zoom_start=12)  # Замените координаты на фактические

# Добавление графиков изменения расхода воды
for index, row in flood_period.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Дата: {index}<br>Расход: {row['Discharge']} м³/с",
        icon=folium.Icon(color='blue')
    ).add_to(m)

m.save("20.html")