import pandas as pd
import geopandas as gpd
from folium import Map, Marker

# Шаг 1: Подготовка данных
df = pd.read_csv('shilik_temperature.csv')

# Шаг 2: Загрузка и очистка данных
df.dropna(inplace=True)

# Шаг 3: Создание географического слоя
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['long'], df['lat']))

# Шаг 4: Объединение данных и создание моделирования
merged_df = pd.merge(gdf, df[['year', 'temperature']], on=['year'])

# Создадим модель для сравнения исторических показателей температуры воды
model = merged_df.groupby('geometry').agg({'temperature': ['mean', 'count']})

# Шаг 5: Визуализация результатов на карте
m = Map(location=[46.75, 76.25], zoom_start=10)
for index, row in model.iterrows():
    Marker(location=index.centroid.coords[0], popup=f'Средняя температура {row["temperature"]["mean"]}, количество наблюдений: {row["temperature"]["count"]}').add_to(m)

m.save("53.html")