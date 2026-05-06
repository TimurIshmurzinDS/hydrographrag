import pandas as pd
import folium

# 1. Получение данных с датчиков
data = pd.read_csv("sensor_data.csv") # Заменить "sensor_data.csv" на актуальный источник данных

# 2. Проверка наличия оповещений
alert_threshold = 5  # Задать порог для оповещения

alerts = data[data["water_level"] > alert_threshold]

if not alerts.empty:
    print("Оповещение о превышении уровня воды!")
    print(alerts)

# 3. Визуализация данных (необязательно)
m = folium.Map(location=[45, 80], zoom_start=10) # Заменить координаты на центр бассейна реки Или

for index, row in data.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Уровень: {row['water_level']}").add_to(m)

m.save("144.html")