import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from folium import Map, Marker

# Загрузим данные о местоположении датчиков и их статусе в виде таблицы.
data = {
    'id': [1, 2, 3],
    'name': ['Датчик 1', 'Датчик 2', 'Датчик 3'],
    'latitude': [55.1234, 55.4567, 55.7890],
    'longitude': [36.9012, 37.2345, 37.5678],
    'signal_status': ['присутствует', 'отсутствует', 'присутствует']
}
df = pd.DataFrame(data)

# Создадим географические объекты для рек Лепсы и Киши Осек на основе их координат.
lepsha_river = gpd.GeoDataFrame(
    geometry=gpd.points_from_xy([36.9012, 37.2345], [55.1234, 55.4567]),
    crs='EPSG:4326'
)
kishi_osok_river = gpd.GeoDataFrame(
    geometry=gpd.points_from_xy([37.5678, 37.8901], [55.7890, 56.0123]),
    crs='EPSG:4326'
)

# Используем функцию st_intersects для определения, где датчики находятся в зоне покрытия сигнала или нет.
lepsha_river['signal_status'] = lepsha_river.apply(lambda row: 'присутствует' if df.loc[df['id'] == row['geometry'].x]['signal_status'].values[0] == 'присутствует' else 'отсутствует', axis=1)
kishi_osok_river['signal_status'] = kishi_osok_river.apply(lambda row: 'присутствует' if df.loc[df['id'] == row['geometry'].x]['signal_status'].values[0] == 'присутствует' else 'отсутствует', axis=1)

# Анализируем результаты и определяем периоды отсутствия сигнала.
lepsha_absence_periods = lepsha_river[lepsha_river['signal_status'] == 'отсутствует']
kishi_osok_absence_periods = kishi_osok_river[kishi_osok_river['signal_status'] == 'отсутствует']

# Создадим карту с периодами отсутствия сигнала.
m = Map(location=[55.5, 37.0], zoom_start=10)
for index, row in lepsha_absence_periods.iterrows():
    Marker(row.geometry.x, row.geometry.y).add_to(m)
for index, row in kishi_osok_absence_periods.iterrows():
    Marker(row.geometry.x, row.geometry.y).add_to(m)

# Сохраняем карту в файл.
m.save("149.html")