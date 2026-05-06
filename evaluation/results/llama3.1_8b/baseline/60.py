import pandas as pd
import geopandas as gpd
from folium import Map, Marker

# Шаг 1: Подготовка данных
osadki = pd.read_csv('osadki.csv')
uroven_vody = pd.read_csv('uroven_vody.csv')

# Шаг 2: Преобразование данных
gdf_osadki = gpd.GeoDataFrame(osadki, geometry=gpd.points_from_xy(osadki['x'], osadki['y']))
gdf_uroven_vody = gpd.GeoDataFrame(uroven_vody, geometry=gpd.points_from_xy(uroven_vody['x'], uroven_vody['y']))

# Шаг 3: Создание географической базы данных
gdf_reka_kara_kara = gpd.read_file('reka_kara_kara.shp')

# Шаг 4: Моделирование влияния осадков на уровень воды
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(gdf_osadki[['osadok']], gdf_uroven_vody['uroven'])

# Шаг 5: Визуализация результатов
m = Map(location=[40, 50], zoom_start=6)
for i in range(len(gdf_reka_kara_kara)):
    marker = Marker(location=gdf_reka_kara_kara.geometry.iloc[i].coords[:2], popup='Уровень воды: ' + str(model.predict(gdf_osadki[['osadok']].iloc[i])))
    m.add_child(marker)
m.save("60.html")