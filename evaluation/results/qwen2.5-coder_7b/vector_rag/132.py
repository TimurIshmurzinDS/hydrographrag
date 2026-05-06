import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна (если необходимо)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровнях воды (замените на реальные данные)
water_level_data = [
    {'date': '2018-01-01', 'river': 'Lepsy River', 'value': 50},
    {'date': '2019-01-01', 'river': 'Lepsy River', 'value': 60},
    {'date': '2020-01-01', 'river': 'Lepsy River', 'value': 70},
    {'date': '2018-01-01', 'river': 'Tekes River', 'value': 45},
    {'date': '2019-01-01', 'river': 'Tekes River', 'value': 55},
    {'date': '2020-01-01', 'river': 'Tekes River', 'value': 65}
]

# Преобразование данных в DataFrame
import pandas as pd
df = pd.DataFrame(water_level_data)
df['date'] = pd.to_datetime(df['date'])

# Группировка по рекам и нахождение максимального значения уровня воды
max_levels = df.groupby('river')['value'].idxmax()
max_dates = df.loc[max_levels, 'date']

# Вывод результатов
print(f"Год с самым высоким уровнем стока в Lepsy River: {max_dates['Lepsy River'].year}")
print(f"Год с самым высоким уровнем стока в Tekes River: {max_dates['Tekes River'].year}")

# Сохранение карты
m.save("132.html")