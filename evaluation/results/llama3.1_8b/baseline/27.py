import pandas as pd
from folium import Map, Marker
import geopandas as gpd

# Загрузите данные о расходе воды в реке Батарейка за различные годы.
data = {
    'Year': [2015, 2016, 2017, 2018],
    'Flow Rate (m3/s)': [10.2, 12.1, 9.5, 11.3]
}
df = pd.DataFrame(data)

# Подготовьте данные к анализу.
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Year'], df['Flow Rate (m3/s)']))

# Определите область весеннего таяния и вычислите расход воды в этой области.
# Для простоты предположим, что область весеннего таяния представляет собой прямоугольник с координатами [45.0, 55.0] x [30.0, 40.0].
area = gpd.GeoDataFrame(geometry=[gpd.Polygon([(45.0, 30.0), (45.0, 40.0), (55.0, 40.0), (55.0, 30.0)])])

# Вычислите расход воды в области весеннего таяния.
flow_rate = gdf[gdf.geometry.x.isin(area.geometry[0].bounds['min': 'max']) & 
                gdf.geometry.y.isin(area.geometry[0].bounds['min': 'max'])]['Flow Rate (m3/s)'].mean()

# Создайте карту с помощью библиотеки Folium.
m = Map(location=[50.0, 35.0], zoom_start=6)
Marker(location=[50.0, 35.0], popup=f'Расход воды в реке Батарейка: {flow_rate} м3/с').add_to(m)

# Сохраните карту.
m.save("27.html")