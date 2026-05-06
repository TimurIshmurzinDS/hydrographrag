import pandas as pd
import geopandas as gpd
from folium import Map, GeoJson


# Загрузка данных о расходе воды
data = pd.read_csv("hydroposts_data.csv")

# Расчет среднего значения расхода воды за период времени без весеннего половодья
mean_flow = data[data["season"] != "spring"]["flow"].mean()

# Определение порога резкого роста расхода воды
threshold = mean_flow * 1.2

# Идентификация событий резкого роста расхода воды
events = data[(data["season"] == "spring") & (data["flow"] > threshold)]

# Загрузка данных о местоположении гидропостов
hydroposts = gpd.read_file("hydroposts_locations.shp")

# Создание карты с помощью folium
m = Map(location=[events["latitude"].mean(), events["longitude"].mean()], zoom_start=12)

# Добавление данных о гидропостах на карту
GeoJson(data=hydroposts, name="hydroposts").add_to(m)

# Добавление данных о событиях резкого роста расхода воды на карту
for index, row in events.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Flow: {row['flow']}").add_to(m)

# Сохранение карты в файл
m.save("84.html")