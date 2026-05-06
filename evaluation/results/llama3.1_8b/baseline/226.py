import folium
import pandas as pd

# Данные о уровне воды в реке Шарын (предположим, что они взяты из API GIS)
water_level_data = {
    'Шарын': [5.2, 4.8, 6.1, 3.9],
    'Долгота': [75.12, 74.98, 76.01, 73.99],
    'Широта': [42.11, 41.97, 43.01, 40.99]
}

# Создаем DataFrame из данных
water_level_df = pd.DataFrame(water_level_data)

# Создаем карту с помощью folium
m = folium.Map(location=[water_level_df['Широта'].mean(), water_level_df['Долгота'].mean()], zoom_start=10)

# Добавляем слой на карте для визуализации данных
folium.Choropleth(
    geo_data='path/to/geojson/file',
    name='Water Level',
    data=water_level_df,
    columns=['Шарын', 'Долгота', 'Широта'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

# Добавляем легенду для слоя
folium.LayerControl().add_to(m)

# Сохраним карту в файле HTML
m.save("226.html")