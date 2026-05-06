import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data_2015 = {
    'date': ['2015-01-01', '2015-02-01', '2015-03-01'],
    'level': [1.2, 1.5, 1.8]
}

data_2023 = {
    'date': ['2023-01-01', '2023-02-01', '2023-03-01'],
    'level': [1.4, 1.7, 2.0]
}

# Преобразование данных в DataFrame
df_2015 = pd.DataFrame(data_2015)
df_2023 = pd.DataFrame(data_2023)

# Нахождение пиковых уровней воды
peak_level_2015 = df_2015['level'].max()
peak_level_2023 = df_2023['level'].max()

print(f"Пиковый уровень воды в 2015 году: {peak_level_2015}")
print(f"Пиковый уровень воды в 2023 году: {peak_level_2023}")

# Создание карты
m = folium.Map(location=[54.687, 39.762], zoom_start=10)

# Добавление точек с пиковыми уровнями воды
folium.Marker(
    location=[54.687, 39.762],
    popup=f"Пиковый уровень в 2015 году: {peak_level_2015}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

folium.Marker(
    location=[54.687, 39.762],
    popup=f"Пиковый уровень в 2023 году: {peak_level_2023}",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("49.html")