import pandas as pd
import numpy as np
import folium

# Шаг 1: Сбор данных (пример синтетических данных)
# Предположим, что у нас есть данные о расходе воды в реке Karatal за определенный период времени.
data = {
    'date': pd.date_range(start='2023-01-01', periods=365),
    'discharge': np.random.uniform(low=10, high=100, size=365)  # расход воды в кубических метрах в секунду
}
df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Шаг 2: Обработка данных
# Удаление пропусков (если есть) и аномалий (значения, выходящие за пределы допустимого диапазона).
df.dropna(inplace=True)
df = df[(df['discharge'] > 0) & (df['discharge'] < 200)]

# Шаг 3: Анализ данных
# Вычисление среднего расхода воды.
mean_discharge = df['discharge'].mean()
print(f"Средний расход воды в реке Karatal: {mean_discharge} м³/с")

# Шаг 4: Моделирование
# Предположим, что для приготовления супа требуется 10 литров воды.
required_water_volume = 10 / 1000  # переводим литры в кубические метры

# Определяем количество секунд, необходимых для набора нужного объема воды
time_required_seconds = required_water_volume / mean_discharge
print(f"Необходимое время для набора воды: {time_required_seconds} секунд")

# Шаг 5: Визуализация данных на карте
# Координаты реки Karatal (примерные)
karatal_coords = [42.8603, 79.1843]

# Создание карты с помощью folium
m = folium.Map(location=karatal_coords, zoom_start=10)

# Добавление маркера на карте
folium.Marker(
    location=karatal_coords,
    popup='Karatal River',
    icon=folium.Icon(icon="info-sign")
).add_to(m)

# Шаг 6: Сохранение карты в файл HTML
m.save("214.html")

print("Карта сохранена как 214.html")