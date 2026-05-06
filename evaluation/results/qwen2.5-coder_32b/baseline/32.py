import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

# Предположим, что у нас есть данные о качестве воды в формате CSV
# Структура данных: Дата, Широта, Долгота, pH, Температура, ЭКС (Электропроводность), Оксиген

# Загрузка данных
data = pd.read_csv('water_quality_talgar.csv')

# Предварительная обработка данных
data.dropna(inplace=True)  # Удаление строк с пропусками
data['Дата'] = pd.to_datetime(data['Дата'])  # Преобразование столбца даты

# Пример статистического анализа: средние значения параметров воды
mean_pH = data['pH'].mean()
mean_temperature = data['Температура'].mean()
mean_EC = data['ЭКС'].mean()
mean_oxygen = data['Оксиген'].mean()

print(f"Среднее pH: {mean_pH}")
print(f"Средняя температура: {mean_temperature} °C")
print(f"Средняя электропроводность: {mean_EC} мкСм/см")
print(f"Средний уровень кислорода: {mean_oxygen} мг/л")

# Создание интерактивной карты с тепловым картографированием
m = folium.Map(location=[43.25, 76.9], zoom_start=10)

# Добавление теплового слоя на основе данных о качестве воды
heat_data = data[['Широта', 'Долгота']].values.tolist()
HeatMap(heat_data).add_to(m)

# Сохранение карты в файл
m.save("32.html")