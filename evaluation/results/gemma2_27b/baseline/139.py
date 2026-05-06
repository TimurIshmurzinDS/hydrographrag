import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Загрузка данных о датчиках
sensors = pd.read_csv("sensors.csv")
sensors["geometry"] = sensors.apply(lambda row: Point(row["longitude"], row["latitude"]), axis=1)
sensors = gpd.GeoDataFrame(sensors, geometry="geometry", crs="EPSG:4326")

# Загрузка данных о реке Сарыкан
river = gpd.read_file("sarykan.shp")

# Пространственный запрос для поиска датчиков вблизи реки
nearby_sensors = gpd.sjoin(sensors, river, how="inner", op="intersects")

# Анализ временных рядов и выявление аномалий
for index, row in nearby_sensors.iterrows():
    # ... (код для анализа временных рядов датчика)

# Создание карты с folium
m = folium.Map(location=[row["latitude"], row["longitude"]], zoom_start=12)
folium.GeoJson("sarykan.shp").add_to(m)

for index, row in nearby_sensors.iterrows():
    if row["anomalous"]:
        folium.Marker(location=[row["latitude"], row["longitude"]], popup="Anomalous Reading", icon=folium.Icon(color="red")).add_to(m)

# Сохранение карты
m.save("139.html")