import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Загрузка данных о бассейнах рек
rivers_shaaryn = gpd.read_file("shaaryn_basin.shp")
rivers_urzhar = gpd.read_file("urzhar_basin.shp")

# Загрузка данных об экологическом статусе (пример)
ecological_data = pd.read_csv("ecological_data.csv")

# Слияние данных о бассейнах и экологическом статусе
rivers_shaaryn = rivers_shaaryn.merge(ecological_data, on="river_id", how="left")
rivers_urzhar = rivers_urzhar.merge(ecological_data, on="river_id", how="left")

# Расчет средних значений индикаторов по бассейнам
mean_indicators_shaaryn = rivers_shaaryn.groupby("basin").mean()
mean_indicators_urzhar = rivers_urzhar.groupby("basin").mean()

# Создание карты с folium
m = folium.Map(location=[43, 78], zoom_start=8)

# Добавление данных о бассейнах на карту
folium.GeoJson(rivers_shaaryn).add_to(m)
folium.GeoJson(rivers_urzhar).add_to(m)

# Добавление информации о средних значениях индикаторов на карту
for index, row in mean_indicators_shaaryn.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Basin: Shaaryn\nIndicator: {row['indicator']} \nMean Value: {row['mean']}")

for index, row in mean_indicators_urzhar.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Basin: Urzhar\nIndicator: {row['indicator']} \nMean Value: {row['mean']}")

# Сохранение карты
m.save("188.html")