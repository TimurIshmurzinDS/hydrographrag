import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файлы с данными о расходе воды и уровне воды.
tokyraun_data = pd.read_csv('tokyraun_discharge.csv', parse_dates=['date'])
koktal_data = pd.read_csv('koktal_level.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
# Удаление пропусков
tokyraun_data.dropna(inplace=True)
koktal_data.dropna(inplace=True)

# Выравнивание временных рядов по дате
merged_data = pd.merge(tokyraun_data, koktal_data, on='date', suffixes=('_tokyraun', '_koktal'))

# Шаг 3: Анализ временных рядов
plt.figure(figsize=(14, 7))
plt.plot(merged_data['date'], merged_data['discharge_tokyraun'], label='Расход воды в Tokyraun River')
plt.plot(merged_data['date'], merged_data['level_koktal'], label='Уровень воды в Koktal River')
plt.xlabel('Дата')
plt.ylabel('Значение показателя')
plt.title('Сравнение расхода воды и уровня воды')
plt.legend()
plt.show()

# Шаг 4: Сравнение показателей
correlation, _ = pearsonr(merged_data['discharge_tokyraun'], merged_data['level_koktal'])
print(f'Корреляция между расходом воды в Tokyraun River и уровнем воды в Koktal River: {correlation}')

# Шаг 5: Оценка риска затопления
# Предположим, что если корреляция выше определенного порога (например, 0.8), риск затопления высок.
risk_threshold = 0.8
if correlation > risk_threshold:
    print('Риск затопления высок.')
else:
    print('Риск затопления низкий.')

# Шаг 6: Визуализация результатов на карте
m = folium.Map(location=[42.5, 79], zoom_start=10)

# Добавление маркеров для рек
folium.Marker([42.38, 79.1], popup='Tokyraun River').add_to(m)
folium.Marker([42.6, 79.2], popup='Koktal River').add_to(m)

m.save("80.html")