import folium
import pandas as pd

# Загрузка данных о датчиках
sensors = pd.read_csv("sensors.csv")

# Загрузка данных о приеме данных
data_reception = pd.read_csv("data_reception.csv")

# Проверка ошибок и добавление информации о статусе датчика
sensors["status"] = "OK"
for index, row in sensors.iterrows():
    sensor_id = row["id"]
    received_data = data_reception[data_reception["sensor_id"] == sensor_id]

    if len(received_data) == 0:
        sensors.loc[index, "status"] = "No Data"
    elif any(pd.isnull(received_data["value"])):
        sensors.loc[index, "status"] = "Error"

# Создание карты с помощью folium
m = folium.Map(location=[43.15, 76.8], zoom_start=10)

for index, row in sensors.iterrows():
    if row["status"] == "OK":
        folium.Marker(location=[row["latitude"], row["longitude"]], popup="Sensor ID: " + str(row["id"]) + ", Status: OK").add_to(m)
    elif row["status"] == "No Data":
        folium.Marker(location=[row["latitude"], row["longitude"]], popup="Sensor ID: " + str(row["id"]) + ", Status: No Data", icon=folium.Icon(color='red')).add_to(m)
    else:
        folium.Marker(location=[row["latitude"], row["longitude"]], popup="Sensor ID: " + str(row["id"]) + ", Status: Error", icon=folium.Icon(color='orange')).add_to(m)

# Сохранение карты
m.save("147.html")