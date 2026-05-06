import pandas as pd
import folium

# Шаг 1: Загрузить исторические данные о весеннем паводке для реки Прохождение.
historical_data = pd.read_csv('prokhodnaya_river_historical.csv')

# Шаг 2: Загрузить текущие данные о расходе на реке Прохождение.
current_data = pd.read_csv('prokhodnaya_river_current.csv')

# Шаг 3: Сравнить исторические и текущие данные, чтобы определить любые изменения в расходе.
merged_data = pd.merge(historical_data, current_data, on='date', suffixes=('_historical', '_current'))

# Шаг 4: Визуализировать результаты на карте с помощью библиотеки Folium.
m = folium.Map(location=[55.76, 37.62], zoom_start=12)

# Добавить слой для отображения исторических данных
folium.Choropleth(
    geo_data='prokhodnaya_river_historical.geojson',
    data=historical_data,
    columns=['date', 'value'],
    key_on='feature.properties.date',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

# Добавить слой для отображения текущих данных
folium.Choropleth(
    geo_data='prokhodnaya_river_current.geojson',
    data=current_data,
    columns=['date', 'value'],
    key_on='feature.properties.date',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

# Добавить слой для отображения изменений в расходе
folium.Choropleth(
    geo_data='prokhodnaya_river_changes.geojson',
    data=merged_data,
    columns=['date', 'value_historical', 'value_current'],
    key_on='feature.properties.date',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

# Сохранить карту в файл
m.save("87.html")