import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, GeoJson

# Загрузка данных о уровне стока
data_kurty = pd.read_csv("kurty_river_flow.csv")
data_urzhar = pd.read_csv("urzhar_river_flow.csv")

# Расчет изменений уровня стока
data_kurty["change"] = data_kurty["flow"].pct_change() * 100
data_urzhar["change"] = data_urzhar["flow"].pct_change() * 100

# Определение порога стресса (например, -20%)
stress_threshold = -20

# Выделение периодов стресса
stress_kurty = data_kurty[data_kurty["change"] < stress_threshold]
stress_urzhar = data_urzhar[data_urzhar["change"] < stress_threshold]

# Загрузка геоданных рек (GeoJSON формат)
rivers_geojson = GeoJson("rivers.geojson")

# Создание карты Folium
m = Map(location=[45, 60], zoom_start=8)

# Добавление данных о стрессе на карту
for index, row in stress_kurty.iterrows():
    plt.plot(row["longitude"], row["latitude"], marker="o", color="red")

for index, row in stress_urzhar.iterrows():
    plt.plot(row["longitude"], row["latitude"], marker="o", color="yellow")

# Добавление рек на карту
rivers_geojson.add_to(m)

# Сохранение карты
m.save("108.html")