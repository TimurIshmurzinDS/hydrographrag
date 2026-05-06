import pandas as pd
import folium

# Загрузка данных о работе датчиков
data = pd.read_csv("sensor_data.csv")

# Преобразование данных в удобный формат
df = data[["timestamp", "sensor_id", "latitude", "longitude", "status"]]

# Расчет времени работы каждого датчика
df["time_working"] = df.groupby("sensor_id").apply(lambda x: x.loc[x["status"] == 1].shape[0])

# Определение коэффициента доступности
df["availability"] = df["time_working"] / len(df) * 100

# Создание карты с folium
m = folium.Map(location=[43.25, 78.25], zoom_start=8)

# Добавление датчиков на карту
for index, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"Sensor ID: {row['sensor_id']}<br>Availability: {row['availability']:.2f}%",
        icon=folium.Icon(color="green" if row["availability"] > 90 else "red")
    ).add_to(m)

# Сохранение карты
m.save("140.html")