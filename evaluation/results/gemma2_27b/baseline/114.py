import pandas as pd
import geopandas as gpd
from folium import Map, GeoJson


# Загрузка данных о дебите рек (замените на ваши данные)
debits = pd.read_csv("river_data.csv")

# Загрузка геоданных рек (замените на ваши данные)
rivers = gpd.read_file("rivers.shp")

# Расчет ирригационного потенциала
rivers["irrigation_potential"] = debits["flow"] / rivers["area"]

# Создание карты с folium
m = Map(location=[40, 60], zoom_start=8)

# Визуализация рек на карте
GeoJson(data=rivers.to_crs("EPSG:4326"), name="Rivers", style_function=lambda feature: {
    "fillColor": "green" if feature["properties"]["irrigation_potential"] > 10 else "red",
    "color": "black",
    "weight": 2,
}).add_to(m)

# Сохранение карты
m.save("114.html")