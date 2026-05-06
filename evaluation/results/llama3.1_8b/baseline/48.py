import pandas as pd
import geopandas as gpd
from folium import Map, Marker

# Шаг 1: Сбор и подготовка данных
data = {
    'Год': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
    'Расход воды (млн. м³)': [10, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35]
}

df = pd.DataFrame(data)

# Добавляем геометрию реки Кара-Кара
river_geom = gpd.read_file('karkara_river.shp')
df_gdf = gpd.GeoDataFrame(df, geometry=river_geom.geometry)

# Шаг 2: Анализ данных
print("Анализ расхода воды:")
print(df_gdf.groupby('Год')['Расход воды (млн. м³)'].mean())

# Шаг 3: Моделирование
from sklearn.linear_model import LinearRegression

X = df_gdf['Год'].values.reshape(-1, 1)
y = df_gdf['Расход воды (млн. м³)']

model = LinearRegression()
model.fit(X, y)

# Шаг 4: Визуализация
m = Map(location=[45.0, 50.0], zoom_start=6)
for index, row in df_gdf.iterrows():
    Marker(row.geometry.y, row.geometry.x).add_to(m)

# Сохраняем карту в HTML-файл
m.save("48.html")