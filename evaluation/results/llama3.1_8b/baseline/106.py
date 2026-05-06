import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import folium

# Загрузим данные о уровнях воды в реках за последние 30 дней
water_levels = pd.read_csv('water_levels.csv', index_col='date', parse_dates=['date'])

# Определим период среза (сезон) на основе данных о температуре и осадках
season_start = datetime.now() - timedelta(days=30)
season_end = season_start + timedelta(days=30)

# Проанализируем данные о уровнях воды в реках для каждого дня периода среза
water_levels_season = water_levels[(water_levels.index >= season_start) & (water_levels.index <= season_end)]

# Оценим, достаточно ли уровней воды в реках для орошения, сравнив их с минимальными требованиями к водному ресурсу
min_water_requirement = 10  # м3/сек
sufficient_water_levels = water_levels_season['level'] >= min_water_requirement

# Визуализируем результаты на карте с помощью библиотеки Folium
m = folium.Map(location=[45.0, 75.0], zoom_start=10)

folium.Choropleth(
    geo_data='geojson/river_boundaries.geojson',
    data=sufficient_water_levels,
    columns=['level', 'sufficient'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

folium.Marker([45.0, 75.0], popup='Сарыкан').add_to(m)
folium.Marker([46.0, 76.0], popup='Аксу').add_to(m)

m.save("106.html")