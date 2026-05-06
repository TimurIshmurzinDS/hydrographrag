import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Сбор и подготовка данных
data = {
    'зона': ['Зона 1', 'Зона 2', 'Зона 3'],
    'объем_забора': [100, 200, 300],
    'место_забора': [(45.123, 37.456), (48.789, 32.111), (42.345, 29.876)]
}

df = pd.DataFrame(data)

# Добавляем геометрию в DataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['место_забора'].apply(lambda x: x[0]), df['место_забора'].apply(lambda x: x[1])))

# Анализ влияния интенсивного забора воды на биоразнообразие
gdf['рисковая_зона'] = gdf.apply(lambda row: 'high_risk' if row['объем_забора'] > 200 else 'low_risk', axis=1)

# Моделирование динамики изменения биоразнообразия
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

X = gdf[['объем_забора']]
y = gdf['рисковая_зона']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

# Предсказание риска изменения биоразнообразия
predictions = model.predict(X_test)

# Визуализация результатов на карте
m = folium.Map(location=[45.123, 37.456], zoom_start=10)
folium.Choropleth(
    geo_data=gdf,
    name='Рисковая зона',
    data=gdf,
    columns=['зона', 'рисковая_зона'],
    key_on='feature.properties.зона',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

m.save("191.html")