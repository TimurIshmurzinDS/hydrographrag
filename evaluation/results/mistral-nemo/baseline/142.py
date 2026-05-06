import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Загрузим данные о местоположении оборудования и его статусе (работает/не работает)
data = {
    'id': [1, 2, 3],
    'geometry': [Point(18.0, 54.0), Point(19.0, 53.5), Point(17.5, 54.5)],
    'status': ['working', 'not_working', 'working']
}

# 2. Создадим точечный векторный слой для каждого объекта мониторинга
gdf = gpd.GeoDataFrame(data, geometry='geometry')

# 3. Проведем анализ данных, чтобы определить, есть ли сбои в работе оборудования
not_working_devices = gdf[gdf['status'] == 'not_working']

# 4. Визуализируем результаты на карте с использованием библиотеки `folium`
m = folium.Map(location=[53.91, 18.0], zoom_start=12)

for idx, row in not_working_devices.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# 5. Сохраним финальную карту как "142.html"
m.save("142.html")