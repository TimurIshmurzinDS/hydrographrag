import pandas as pd
import numpy as np
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла CSV:
# - 'aksu_water_flow.csv' с данными о расходе воды в реке Аксу (дата, расход)
# - 'agricultural_plots.csv' с данными о месторасположении и потребностях сельскохозяйственных угодий (широта, долгота, потребность_воды)

# Загрузка данных
water_flow_data = pd.read_csv('aksu_water_flow.csv', parse_dates=['date'])
agricultural_plots_data = pd.read_csv('agricultural_plots.csv')

# Шаг 2: Препроцессинг данных
# Обработка пропущенных значений и нормализация данных
water_flow_data.fillna(method='ffill', inplace=True)
agricultural_plots_data.dropna(inplace=True)

# Вычисление среднего месячного расхода воды для анализа
monthly_water_flow = water_flow_data.resample('M', on='date').mean().reset_index()

# Шаг 3: Моделирование
# Предположим, что потребность в воде сельскохозяйственных угодий постоянна и известна.
# Мы можем оценить общий объем воды, забираемой сельским хозяйством за месяц.

total_monthly_water_demand = agricultural_plots_data['потребность_воды'].sum()

# Шаг 4: Визуализация
# Создание карты с использованием folium
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты Бишкека

# Добавление маркеров для сельскохозяйственных угодий на карту
for _, row in agricultural_plots_data.iterrows():
    folium.Marker(
        location=[row['широта'], row['долгота']],
        popup=f"Потребность в воде: {row['потребность_воды']} м³/мес",
        icon=folium.Icon(color='green')
    ).add_to(m)

# Сохранение карты
m.save("33.html")

# Вывод результата
print(f"Общий объем воды, забираемой сельским хозяйством за месяц: {total_monthly_water_demand} м³")