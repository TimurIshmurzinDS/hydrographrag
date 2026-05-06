import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузим данные о расходе воды в реке Курты за прошлые годы.
data = {
    'date': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01',
             '2020-06-01', '2020-07-01', '2020-08-01', '2020-09-01', '2020-10-01',
             '2020-11-01', '2020-12-01'],
    'water_flow': [100, 120, 150, 180, 200, 220, 250, 280, 300, 320, 350, 380],
    'season': ['зима', 'зима', 'весна', 'лето', 'лето', 'лето', 'лето', 'осень', 'осень',
               'осень', 'зима', 'зима']
}
df = pd.DataFrame(data)

# Разделим данные на летние и зимние периоды.
summer_df = df[df['season'] == 'лето']
winter_df = df[df['season'] == 'зима']

# Рассчитаем средний расход воды для каждого периода.
summer_avg_flow = summer_df['water_flow'].mean()
winter_avg_flow = winter_df['water_flow'].mean()

print(f'Средний расход воды в летний период: {summer_avg_flow}')
print(f'Средний расход воды в зимний период: {winter_avg_flow}')

# Сравним средние значения расхода воды для обоих периодов.
if summer_avg_flow > winter_avg_flow:
    print('Расход воды в летний период больше, чем в зимний.')
elif summer_avg_flow < winter_avg_flow:
    print('Расход воды в зимний период больше, чем в летний.')
else:
    print('Расход воды в летний и зимний периоды одинаковый.')

# Визуализируем результаты на карте.
m = folium.Map(location=[55.75, 60], zoom_start=10)
folium.Marker([55.75, 60], popup='Курты', icon=folium.Icon(color='blue')).add_to(m)

# Добавим слой с данными о расходе воды.
summer_gdf = gpd.GeoDataFrame(summer_df, geometry=gpd.points_from_xy(summer_df['water_flow'], summer_df['date']))
winter_gdf = gpd.GeoDataFrame(winter_df, geometry=gpd.points_from_xy(winter_df['water_flow'], winter_df['date']))

folium.Choropleth(
    geo_data=winter_gdf,
    name='Зимний период',
    data=winter_gdf,
    columns=['water_flow', 'date'],
    key_on='feature.properties.water_flow',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

folium.Choropleth(
    geo_data=summer_gdf,
    name='Летний период',
    data=summer_gdf,
    columns=['water_flow', 'date'],
    key_on='feature.properties.water_flow',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

m.save("51.html")