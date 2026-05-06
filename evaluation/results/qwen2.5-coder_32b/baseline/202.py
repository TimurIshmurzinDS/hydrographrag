import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть данные о стоке рек в формате CSV с колонками: 'date', 'Emel_Discharge', 'Turgen_Discharge'
data = pd.read_csv('river_discharge_data.csv', parse_dates=['date'], index_col='date')

# Проверка первых строк данных
print(data.head())

# Предобработка данных (заполнение пропусков, удаление аномалий)
data.fillna(method='ffill', inplace=True)

# Вычисление статистических показателей для каждой реки
emel_stats = data['Emel_Discharge'].describe()
turgen_stats = data['Turgen_Discharge'].describe()

print("Статистика по Реке Эмел:")
print(emel_stats)
print("\nСтатистика по Реке Турген:")
print(turgen_stats)

# Вычисление коэффициента вариации для каждой реки
emel_cv = emel_stats['std'] / emel_stats['mean']
turgen_cv = turgen_stats['std'] / turgen_stats['mean']

print(f"\nКоэффициент вариации для Реки Эмел: {emel_cv}")
print(f"Коэффициент вариации для Реки Турген: {turgen_cv}")

# Определение реки с более значительной межгодовой изменчивостью
if emel_cv > turgen_cv:
    more_variable_river = "Emel River"
else:
    more_variable_river = "Turgen River"

print(f"\nРека с более значительной межгодовой изменчивостью стока: {more_variable_river}")

# Визуализация данных на карте
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерно по центру Кыргызстана

# Добавление маркеров для рек (координаты могут быть изменены на точные)
folium.Marker([42.8673, 75.9250], popup='Emel River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([42.8117, 74.5910], popup='Turgen River', icon=folium.Icon(color='green')).add_to(m)

# Добавление информации о более изменчивой реке
folium.Marker(
    [42.8746, 74.5910],
    popup=f"Река с более значительной межгодовой изменчивостью стока: {more_variable_river}",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты
m.save("202.html")

# Построение графиков временных рядов для визуального сравнения
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['Emel_Discharge'], label='Река Эмел', color='blue')
plt.plot(data.index, data['Turgen_Discharge'], label='Река Турген', color='green')
plt.title('Сравнение стока рек по годам')
plt.xlabel('Год')
plt.ylabel('Сток (куб. м/с)')
plt.legend()
plt.grid(True)
plt.show()