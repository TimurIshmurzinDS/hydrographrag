import pandas as pd
import geopandas as gpd
from folium import Map, Marker, CircleMarker
from folium.plugins import HeatMap

# Загрузите данные о датчиках уровня воды и аномальных показателях
датчики = pd.read_csv('датчики.csv')
аномальные_показатели = pd.read_csv('аномальные_показатели.csv')

# Создайте слой для отображения реки Сарыкан на карте
сарыкан = gpd.read_file('сарыкан.shp')
карта = Map(location=[сарыкан.centroid.y, сарыкан.centroid.x], zoom_start=10)

# Добавьте слой для отображения местоположений датчиков уровня воды
for index, row in датчики.iterrows():
    Marker([row['lat'], row['lon']], popup=row['name']).add_to(карта)

# Добавьте слой для отображения аномальных показателей
аномальные_показатели_гео = гpd.GeoDataFrame(аномальные_показатели, geometry=gpd.points_from_xy(аномальные_показатели['lon'], аномальные_показатели['lat']))
HeatMap(аномальные_показатели_гео['value'].values, radius=10).add_to(карта)

# Сохраните карту в файл
карта.save("139.html")