import pandas as pd
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть CSV файлы с данными о уровне воды за 2022 и 2023 годы.
# Формат данных: дата (datetime), уровень_воды (float)

# Шаг 1: Сбор данных
data_2022 = pd.read_csv('sarykan_water_level_2022.csv', parse_dates=['date'])
data_2023 = pd.read_csv('sarykan_water_level_2023.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
data_2022.dropna(inplace=True)
data_2023.dropna(inplace=True)

# Шаг 3: Анализ данных
stats_2022 = data_2022['water_level'].describe()
stats_2023 = data_2023['water_level'].describe()

print("Статистика уровня воды за 2022 год:")
print(stats_2022)
print("\nСтатистика уровня воды за 2023 год:")
print(stats_2023)

# Шаг 4: Визуализация данных
plt.figure(figsize=(14, 7))
plt.plot(data_2022['date'], data_2022['water_level'], label='2022', color='blue')
plt.plot(data_2023['date'], data_2023['water_level'], label='2023', color='green')
plt.title('Уровень воды в реке Сарыкан за 2022 и 2023 годы')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.grid(True)
plt.show()

# Шаг 5: Геоспатиальная визуализация
# Предположим, что у нас есть координаты точек измерений уровня воды.
# Формат данных: дата (datetime), уровень_воды (float), широта (float), долгота (float)

# Пример данных для геоспатиальной визуализации
geo_data = pd.read_csv('sarykan_water_level_geo.csv', parse_dates=['date'])

m = folium.Map(location=[42.8746, 75.0931], zoom_start=10)  # Координаты Бишкека

for _, row in geo_data.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['water_level'] * 2,  # Увеличение радиуса для наглядности
        color='blue' if row['date'].year == 2022 else 'green',
        fill=True,
        fill_color='blue' if row['date'].year == 2022 else 'green',
        popup=f"Дата: {row['date']}\nУровень воды: {row['water_level']} м"
    ).add_to(m)

m.save("46.html")