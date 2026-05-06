import pandas as pd
import numpy as np
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла CSV:
# - 'ayagoz_flow.csv' с данными о расходах воды в реке Аягоз (дата, расход)
# - 'irrigation_demand.csv' с данными о потребности в воде для ирригации (дата, объем)

# Загрузка данных
flow_data = pd.read_csv('ayagoz_flow.csv', parse_dates=['date'])
demand_data = pd.read_csv('irrigation_demand.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
# Убедимся, что данные отсортированы по дате и объединены по датам
flow_data.sort_values(by='date', inplace=True)
demand_data.sort_values(by='date', inplace=True)

# Объединение данных по дате
merged_data = pd.merge(flow_data, demand_data, on='date')

# Заполнение пропусков (если есть) и нормализация данных
merged_data.fillna(method='ffill', inplace=True)
merged_data['flow'] = merged_data['flow'].clip(lower=0)
merged_data['demand'] = merged_data['demand'].clip(lower=0)

# Шаг 3: Моделирование дефицита
# Вычисление дефицита воды (разница между спросом и предложением)
merged_data['deficit'] = np.maximum(0, merged_data['demand'] - merged_data['flow'])

# Шаг 4: Визуализация результатов
# Предположим, что у нас есть координаты реки Аягоз (широта и долгота)
latitude = 51.8369  # Примерные координаты реки Аягоз
longitude = 74.2091

# Создание карты с помощью folium
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Добавление тепловой карты для отображения уровня дефицита воды
heat_data = [[row['latitude'], row['longitude'], row['deficit']] for index, row in merged_data.iterrows()]
folium.plugins.HeatMap(heat_data).add_to(m)

# Сохранение карты в файл
m.save("35.html")