import pandas as pd
import folium

# Загрузите данные о расходе воды для обоих годов из соответствующих источников
data_2020 = pd.read_csv('sarykan_river_water_discharge_2020.csv')
data_2023 = pd.read_csv('sarykan_river_water_discharge_2023.csv')

# Очистите данные и убедитесь, что они имеют одинаковую структуру и единицы измерения
data_2020['date'] = pd.to_datetime(data_2020['date'])
data_2023['date'] = pd.to_datetime(data_2023['date'])

# Создайте две серии временных рядов, одну для каждого года, используя дату как индекс
ts_2020 = data_2020.set_index('date')['discharge']
ts_2023 = data_2023.set_index('date')['discharge']

# Выполните сравнение между сериями временных рядов с помощью функции `compare` из библиотеки `pandas`
comparison = pd.compare(ts_2020, ts_2023)

# Визуализируйте результаты сравнения на карте с использованием библиотеки `folium`, отмечая местоположение реки и отображая изменения расхода воды в виде цветовой шкалы
m = folium.Map(location=[41.73, 69.28], zoom_start=8)  # Координаты реки Sarykan River

# Отобразите реку на карте
folium.GeoJson(
    data_2020[['geometry']],
    style_function=lambda x: {'fillColor': 'blue', 'color': 'black'},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function=lambda x: {'fillColor': 'yellow'}),
).add_to(m)

# Отобразите изменения расхода воды в виде цветовой шкалы
folium.Choropleth(
    comparison,
    geo_data=data_2020[['geometry']],
    columns=['discharge'],
    key_on='feature.id',
    fill_color='YlGnBu',
    legend_name='Water Discharge Change (m³/s)',
).add_to(m)

# Сохраните карту как HTML-файл
m.save("58.html")