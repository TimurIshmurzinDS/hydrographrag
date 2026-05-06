import pandas as pd
from folium import Map, GeoJson

# Загрузка данных о датчиках
data = pd.read_csv("sensors.csv")

# Расчет времени с последнего обслуживания
data["time_since_last_maintenance"] = pd.to_datetime("today") - pd.to_datetime(data["date_of_last_maintenance"])

# Определение датчиков, нуждающихся в обслуживании
need_maintenance = data[data["time_since_last_maintenance"] > pd.Timedelta(days=180)]

# Создание карты
m = Map(location=[43.25, 79.25], zoom_start=8)

# Визуализация датчиков на карте
GeoJson(data[["latitude", "longitude"]].to_records(index=False), name="sensors").add_to(m)

# Визуализация датчиков, нуждающихся в обслуживании
GeoJson(need_maintenance[["latitude", "longitude"]].to_records(index=False), name="need_maintenance", style_function=lambda feature: {"color": "red"}).add_to(m)

# Сохранение карты
m.save("146.html")