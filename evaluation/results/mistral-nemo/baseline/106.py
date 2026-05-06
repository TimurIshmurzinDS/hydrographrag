import geopandas as gpd
import pandas as pd
import folium

# Шаг 1: Получение данных о уровнях воды в реках
river_data = {
    'Sarykan River': {'current_level': 50, 'threshold': 60},
    'Aksu River': {'current_level': 45, 'threshold': 55}
}

# Шаг 2: Создание DataFrame для хранения данных о реках
rivers_df = pd.DataFrame.from_dict(river_data, orient='index')

# Шаг 3: Сравнение текущих уровней воды с пороговыми значениями и добавление результатов в DataFrame
rivers_df['sufficient_water'] = rivers_df.apply(lambda row: 'Достаточно' if row['current_level'] >= row['threshold'] else 'Недостаточно', axis=1)

# Шаг 4: Визуализация результатов на карте с использованием библиотеки `folium`
m = folium.Map(location=[42.87, 69.95], zoom_start=8)  # Координаты для начала отображения карты

for index, row in rivers_df.iterrows():
    river_name = index
    sufficient_water = row['sufficient_water']
    folium.Marker([row['latitude'], row['longitude']], popup=f'{river_name}: {sufficient_water}').add_to(m)

# Сохранение карты в файл HTML
m.save("106.html")