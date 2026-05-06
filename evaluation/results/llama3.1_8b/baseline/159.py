import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Загрузите данные о реках и их течении
lepsy_river = gpd.read_file('path/to/lepsy_river.shp')
shynzhaly_river = gpd.read_file('path/to/shynzhaly_river.shp')

# Создайте модель перелива воды на основе данных о речном стоке и площади бассейна
def calculate_flood_risk(river):
    river['flood_risk'] = (river['discharge'] / river['basin_area']) * 100
    return river

lepsy_river = calculate_flood_risk(lepsy_river)
shynzhaly_river = calculate_flood_risk(shynzhaly_river)

# Оцените риск перелива во время весеннего таяния на основе данных о температуре воздуха и количестве осадков
def evaluate_flood_risk(river, temperature, precipitation):
    river['flood_risk'] = river['flood_risk'] * (temperature / 10) * (precipitation / 100)
    return river

# Данные о температуре воздуха и количестве осадков в регионе
temperature = 15  # градусов Цельсия
precipitation = 50  # мм

lepsy_river = evaluate_flood_risk(lepsy_river, temperature, precipitation)
shynzhaly_river = evaluate_flood_risk(shynzhaly_river, temperature, precipitation)

# Проанализируйте результаты моделирования и создайте карту с зонами высокого риска перелива
def create_flood_map(rivers):
    m = Map(location=[50.0, 70.0], zoom_start=10)
    
    for index, row in rivers.iterrows():
        if row['flood_risk'] > 100:
            Marker([row['geometry'].y, row['geometry'].x]).add_to(m)
        
    return m

m = create_flood_map(lepsy_river.append(shynzhaly_river))
m.save("159.html")