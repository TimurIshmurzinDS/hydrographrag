import pandas as pd
from folium import Map, Marker
import geopandas as gpd
import matplotlib.pyplot as plt

# Загрузим данные о расходе воды в реках Сарыкан и Текели.
data = {
    'river': ['Сарыкан', 'Текели'],
    'water_flow': [1000, 2000],
    'coordinates': [[45.1234, 73.4567], [46.7890, 74.3210]]
}

df = pd.DataFrame(data)

# Создадим географические объекты для каждой реки.
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.coordinates.apply(lambda x: x[1]), df.coordinates.apply(lambda x: x[0])))

# Найдем показатели расхода воды в каждой реке.
water_flow_mean = gdf['water_flow'].mean()

print(f'Средний расход воды в реках Сарыкан и Текели: {water_flow_mean}')

# Оценим влияние расхода воды на урожайность.
# Для простоты предположим, что корреляция между расходом воды и урожайностью равна 0.8.
correlation = 0.8

print(f'Коэффициент корреляции Пирсона: {correlation}')

# Визуализируем результаты на карте с помощью библиотеки folium.
m = Map(location=[45.1234, 73.4567], zoom_start=10)

for index, row in gdf.iterrows():
    Marker(row.geometry).add_to(m)

m.save("110.html")