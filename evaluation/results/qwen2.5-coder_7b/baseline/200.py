import pandas as pd
import folium

# Загрузка исторических данных о паводках (пример)
historical_data = pd.read_csv('historical_floods.csv')

# Фильтрация данных для участка Kishi Osek
kishi_osek_data = historical_data[historical_data['river'] == 'Kishi Osek']

# Идентификация экстремальных паводков (пример: максимальная высота воды > 10 метров)
extreme_years = kishi_osek_data[kishi_osek_data['max_water_level'] > 10]['year'].unique()

# Загрузка текущих данных с использованием API или другого источника (пример)
current_data = pd.read_csv('current_floods.csv')

# Фильтрация текущих данных для участка Kishi Osek
current_kishi_osek_data = current_data[current_data['river'] == 'Kishi Osek']

# Сравнение текущих показателей с историческими данными (пример: максимальная высота воды)
comparison_results = pd.merge(current_kishi_osek_data, kishi_osek_data, on='year', suffixes=('_current', '_historical'))

# Визуализация данных на карте
m = folium.Map(location=[35.0, 140.0], zoom_start=8)

for index, row in comparison_results.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Year: {row['year']}<br>Max Water Level (Current): {row['max_water_level_current']} m<br>Max Water Level (Historical): {row['max_water_level_historical']} m",
        icon=folium.Icon(color='red' if row['max_water_level_current'] > 10 else 'green')
    ).add_to(m)

# Сохранение карты
m.save("200.html")