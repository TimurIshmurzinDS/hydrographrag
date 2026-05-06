import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
koksu_data = pd.read_csv('Koksu_River_min_levels.csv')
byzhy_data = pd.read_csv('Byzhy_River_min_levels.csv')

# Пример структуры данных:
# koksu_data = pd.DataFrame({
#     'date': pd.date_range(start='1/1/2010', periods=10, freq='Y'),
#     'min_level': [100, 95, 98, 102, 101, 103, 104, 105, 106, 107]
# })

# Пример структуры данных:
# byzhy_data = pd.DataFrame({
#     'date': pd.date_range(start='1/1/2010', periods=10, freq='Y'),
#     'min_level': [85, 90, 93, 97, 96, 98, 100, 101, 102, 103]
# })

# Обработка данных
koksu_data['date'] = pd.to_datetime(koksu_data['date'])
byzhy_data['date'] = pd.to_datetime(byzhy_data['date'])

# Анализ тренда для Koksu River
decomposition_koksu = seasonal_decompose(koksu_data['min_level'], model='additive', period=1)
trend_koksu = decomposition_koksu.trend

# Анализ тренда для Byzhy River
decomposition_byzhy = seasonal_decompose(byzhy_data['min_level'], model='additive', period=1)
trend_byzhy = decomposition_byzhy.trend

# Визуализация данных на карте
m = folium.Map(location=[50, 30], zoom_start=6)

# Добавление точек для Koksu River
for idx, row in koksu_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Koksu River: {row['min_level']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Добавление точек для Byzhy River
for idx, row in byzhy_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Byzhy River: {row['min_level']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("208.html")