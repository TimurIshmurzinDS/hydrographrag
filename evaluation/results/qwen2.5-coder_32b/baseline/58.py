import pandas as pd
import matplotlib.pyplot as plt
import folium

# Предполагается, что данные находятся в CSV файле с колонками: 'date', 'discharge'
# Пример структуры данных:
# date,discharge
# 2020-01-01,150.5
# 2020-01-02,148.3
# ...

# Шаг 1: Сбор данных
data = pd.read_csv('sarykan_river_discharge.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month

# Фильтрация данных за 2020 и 2023 годы
data_2020 = data[data['year'] == 2020]
data_2023 = data[data['year'] == 2023]

# Шаг 3: Анализ данных - вычисление ежемесячных средних значений расхода воды
monthly_avg_2020 = data_2020.groupby('month')['discharge'].mean()
monthly_avg_2023 = data_2023.groupby('month')['discharge'].mean()

# Шаг 4: Визуализация данных
plt.figure(figsize=(12, 6))
plt.plot(monthly_avg_2020.index, monthly_avg_2020.values, label='2020', marker='o')
plt.plot(monthly_avg_2023.index, monthly_avg_2023.values, label='2023', marker='x')
plt.title('Сравнение ежемесячных показателей расхода воды в реке Sarykan River за 2020 и 2023 годы')
plt.xlabel('Месяц')
plt.ylabel('Расход воды (куб. м/с)')
plt.xticks(range(1, 13), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
plt.legend()
plt.grid(True)
plt.savefig('discharge_comparison.png')
plt.show()

# Шаг 5: Географическая визуализация (опционально)
# Предположим, что есть геоданные о местоположении измерительных пунктов
# Пример структуры данных:
# latitude,longitude,discharge_2020,discharge_2023
# 45.123,76.456,150.5,160.2
# ...

# Чтение геоданных
geo_data = pd.read_csv('sarykan_river_geo.csv')

# Создание карты с использованием folium
m = folium.Map(location=[geo_data['latitude'].mean(), geo_data['longitude'].mean()], zoom_start=10)

# Добавление маркеров на карту для каждого измерительного пункта
for _, row in geo_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"2020: {row['discharge_2020']} куб. м/с, 2023: {row['discharge_2023']} куб. м/с",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("58.html")