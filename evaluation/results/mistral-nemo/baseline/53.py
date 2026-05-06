import pandas as pd
import folium

# Загружаем данные о температуре воды для 2021 и 2022 годов из CSV-файлов
data_2021 = pd.read_csv('shilik_river_temperature_2021.csv')
data_2022 = pd.read_csv('shilik_river_temperature_2022.csv')

# Очищаем и предобрабатываем данные (если необходимо)
data_2021.dropna(inplace=True)
data_2022.dropna(inplace=True)

# Создаем две отдельные таблицы для каждого года с данными о температуре воды
df_2021 = pd.DataFrame(data_2021, columns=['latitude', 'longitude', 'temperature'])
df_2022 = pd.DataFrame(data_2022, columns=['latitude', 'longitude', 'temperature'])

# Создаем карту с использованием библиотеки folium
m = folium.Map(location=[43.2, 76.9], zoom_start=8)

# Добавляем данные о температуре воды для 2021 года на карту
for _, row in df_2021.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.7,
        popup=f'Temperature 2021: {row["temperature"]}°C'
    ).add_to(m)

# Добавляем данные о температуре воды для 2022 года на карту
for _, row in df_2022.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='red',
        fill=True,
        fill_opacity=0.7,
        popup=f'Temperature 2022: {row["temperature"]}°C'
    ).add_to(m)

# Сохраняем финальную карту как "53.html"
m.save("53.html")