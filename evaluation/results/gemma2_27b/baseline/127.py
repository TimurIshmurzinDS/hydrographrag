import pandas as pd
import geopandas as gpd
from folium import Map, GeoJson


# Загрузка данных о максимальных уровнях паводков
flood_data = pd.read_csv("flood_levels.csv")

# Загрузка данных о средних исторических уровнях
historical_levels = pd.read_csv("historical_levels.csv")

# Вычисление разницы между уровнями
difference = flood_data["level"] - historical_levels["level"]

# Создание GeoDataFrame для визуализации (если требуется)
geo_data = gpd.GeoDataFrame(data={"difference": difference}, geometry=flood_data["geometry"])

# Визуализация на карте (необязательно)
m = Map(location=[43.1, 78.5], zoom_start=9)
GeoJson(geo_data).add_to(m)
m.save("127.html")