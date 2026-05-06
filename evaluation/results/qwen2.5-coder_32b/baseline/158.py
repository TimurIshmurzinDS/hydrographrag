import pandas as pd
import numpy as np
from scipy import stats
import folium
from datetime import datetime

# Предположим, что у нас есть временные ряды уровня воды для обоих речных систем.
# Для примера создадим синтетические данные.

np.random.seed(42)
dates = pd.date_range(start='1/1/2015', end='31/12/2020')
bayankol_water_level = np.sin(np.linspace(0, 10 * np.pi, len(dates))) + np.random.normal(0, 0.1, len(dates)) * 10
sarykan_water_level = np.cos(np.linspace(0, 10 * np.pi, len(dates))) + np.random.normal(0, 0.1, len(dates)) * 10

bayankol_data = pd.DataFrame({'date': dates, 'water_level': bayankol_water_level})
sarykan_data = pd.DataFrame({'date': dates, 'water_level': sarykan_water_level})

# Преобразуем даты в формат datetime
bayankol_data['date'] = pd.to_datetime(bayankol_data['date'])
sarykan_data['date'] = pd.to_datetime(sarykan_data['date'])

# Определим критерий для определения паводкового периода (например, уровень воды выше среднего на 2 стандартных отклонения)
bayankol_mean = bayankol_data['water_level'].mean()
bayankol_std = bayankol_data['water_level'].std()

sarykan_mean = sarykan_data['water_level'].mean()
sarykan_std = sarykan_data['water_level'].std()

bayankol_flood_periods = bayankol_data[bayankol_data['water_level'] > bayankol_mean + 2 * bayankol_std]
sarykan_flood_periods = sarykan_data[sarykan_data['water_level'] > sarykan_mean + 2 * sarykan_std]

# Определим наиболее опасные периоды (месяцы)
bayankol_flood_months = bayankol_flood_periods['date'].dt.month.value_counts().sort_index()
sarykan_flood_months = sarykan_flood_periods['date'].dt.month.value_counts().sort_index()

# Визуализация на карте
m = folium.Map(location=[43.2684, 79.9015], zoom_start=6)  # Координаты примерно по центру Казахстана

# Добавим маркеры для рек с указанием наиболее опасных периодов
folium.Marker(
    location=[43.2684, 79.9015],  # Примерные координаты Bayankol River
    popup=f"Bayankol River\nНаиболее опасные месяцы: {bayankol_flood_months.idxmax()}",
    icon=folium.Icon(color='red')
).add_to(m)

folium.Marker(
    location=[43.2684, 79.9015],  # Примерные координаты Sarykan River
    popup=f"Sarykan River\nНаиболее опасные месяцы: {sarykan_flood_months.idxmax()}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("158.html")