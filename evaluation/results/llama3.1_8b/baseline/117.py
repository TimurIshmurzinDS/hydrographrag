import pandas as pd
import geopandas as gpd
from folium import Map, Marker, CircleMarker
import matplotlib.pyplot as plt

# Сбор данных
data = {
    'river': ['Урзар', 'Аксай'],
    'flow_change': [10, 20],
    'ecological_balance': [50, 60]
}
df = pd.DataFrame(data)

# Преобразование данных
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['river'].str.get_offsets().apply(lambda x: x[0]), df['river'].str.get_offsets().apply(lambda x: x[1])))

# Создание модели
from sklearn.linear_model import LinearRegression
X = gdf[['flow_change']]
y = gdf['ecological_balance']
model = LinearRegression()
model.fit(X, y)

# Анализ модели
print('Коэффициент корреляции:', model.score(X, y))
print('Значимость факторов:')
print(model.coef_)

# Визуализация результатов
m = Map(location=[50.0, 70.0], zoom_start=6)
for i in range(len(gdf)):
    marker = Marker(location=gdf.iloc[i]['geometry'].coords[0], popup=f'Река: {gdf.iloc[i]["river"]}<br>Изменение стока: {gdf.iloc[i]["flow_change"]} м³/с<br>Экологический баланс: {gdf.iloc[i]["ecological_balance"]} %')
    m.add_child(marker)
m.save("117.html")