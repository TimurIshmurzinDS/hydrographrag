import pandas as pd
from geopandas import GeoDataFrame
from scipy.stats import norm
import folium

# Шаг 1: Загрузка данных
data = {
    'высота_берега': [10, 15, 20],
    'скорость_течения': [2, 3, 4],
    'интенсивность_осадков': [5, 6, 7]
}
df = pd.DataFrame(data)

# Шаг 2: Геопроцессинг данных
gdf = GeoDataFrame(df, geometry=gpd.points_from_xy(df['высота_берега'], df['скорость_течения']))

# Шаг 3: Оценка риска наводнения
def оценка_риска(высота_берега, скорость_течения, интенсивность_осадков):
    # Расчет вероятности наводнения
    mean = (высота_берега + скорость_течения) / 2
    std_dev = интенсивность_осадков
    вероятность = norm.cdf(0, loc=mean, scale=std_dev)
    return вероятность

# Применение функции к каждой записи в данных
gdf['вероятность'] = gdf.apply(lambda row: оценка_риска(row['высота_берега'], row['скорость_течения'], row['интенсивность_осадков']), axis=1)

# Шаг 4: Визуализация результатов
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)
folium.Choropleth(
    geo_data=gdf,
    data=gdf,
    columns=['высота_берега', 'скорость_течения', 'интенсивность_осадков'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
m.save("23.html")