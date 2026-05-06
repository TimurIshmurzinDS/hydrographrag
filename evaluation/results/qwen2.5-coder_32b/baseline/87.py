import pandas as pd
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файлы с данными о расходе воды на реке Прокходная.
# Файл 'current_data.csv' содержит текущие данные, а 'historical_data.csv' - исторические.

# Загрузка данных
current_data = pd.read_csv('current_data.csv', parse_dates=['date'])
historical_data = pd.read_csv('historical_data.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
# Предположим, что данные содержат столбцы 'date' и 'discharge'.

# Фильтрация исторических данных за весенний период (апрель-май)
spring_historical_data = historical_data[(historical_data['date'].dt.month >= 4) & (historical_data['date'].dt.month <= 5)]

# Шаг 3: Анализ данных
# Вычисление среднего и максимального расхода воды за весенний период из исторических данных
mean_discharge = spring_historical_data['discharge'].mean()
max_discharge = spring_historical_data['discharge'].max()

# Сравнение текущего расхода с историческими данными
current_mean_discharge = current_data['discharge'].mean()
is_above_average = current_mean_discharge > mean_discharge

# Шаг 4: Визуализация результатов
# Создание графика для сравнения текущих данных с историческими средними и максимальными значениями
plt.figure(figsize=(12, 6))
plt.plot(spring_historical_data['date'], spring_historical_data['discharge'], label='Исторические данные', alpha=0.5)
plt.axhline(y=mean_discharge, color='r', linestyle='--', label=f'Средний расход: {mean_discharge:.2f}')
plt.axhline(y=max_discharge, color='g', linestyle='--', label=f'Максимальный расход: {max_discharge:.2f}')
plt.plot(current_data['date'], current_data['discharge'], label='Текущие данные', color='b')
plt.title('Сравнение текущего расхода воды с историческими данными')
plt.xlabel('Дата')
plt.ylabel('Расход воды, м³/с')
plt.legend()
plt.grid(True)
plt.show()

# Создание карты для визуализации местоположения реки Прокходная
m = folium.Map(location=[56.129047, 38.383011], zoom_start=12)  # Координаты примерного местоположения реки

# Добавление маркера на карту
folium.Marker(
    location=[56.129047, 38.383011],
    popup='Река Прокходная',
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в HTML файл
m.save("87.html")

# Вывод результата сравнения
print(f"Средний исторический расход воды: {mean_discharge:.2f} м³/с")
print(f"Максимальный исторический расход воды: {max_discharge:.2f} м³/с")
print(f"Текущий средний расход воды: {current_mean_discharge:.2f} м³/с")
if is_above_average:
    print("Текущий средний расход воды выше среднего исторического.")
else:
    print("Текущий средний расход воды ниже или равен среднему историческому.")