import folium
import pandas as pd
import random

# 1. Симуляция данных датчиков на реке Талгар
# Примерные координаты бассейна реки Талгар (Казахстан)
# Река течет примерно с гор Тянь-Шаня в сторону Алматы
sensors_data = [
    {"sensor_id": "TGL-01", "lat": 43.152, "lon": 77.312, "status": "Active", "value": "1.2m"},
    {"sensor_id": "TGL-02", "lat": 43.185, "lon": 77.250, "status": "Warning", "value": "2.5m"},
    {"sensor_id": "TGL-03", "lat": 43.210, "lon": 77.180, "status": "Active", "value": "1.1m"},
    {"sensor_id": "TGL-04", "lat": 43.245, "lon": 77.110, "status": "Inactive", "value": "N/A"},
    {"sensor_id": "TGL-05", "lat": 43.280, "lon": 77.050, "status": "Active", "value": "0.9m"},
    {"sensor_id": "TGL-06", "lat": 43.310, "lon": 76.980, "status": "Warning", "value": "2.1m"},
]

# Преобразование в DataFrame для удобства обработки
df = pd.DataFrame(sensors_data)

# 2. Функция для определения цвета маркера в зависимости от статуса
def get_color(status):
    if status == "Active":
        return "green"
    elif status == "Warning":
        return "orange"
    elif status == "Inactive":
        return "red"
    else:
        return "gray"

# 3. Создание карты
# Центрируем карту на среднем значении координат датчиков
center_lat = df['lat'].mean()
center_lon = df['lon'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles="OpenStreetMap")

# 4. Добавление датчиков на карту
for index, row in df.iterrows():
    # Формируем текст для всплывающего окна
    popup_text = f"<b>Sensor ID:</b> {row['sensor_id']}<br>" \
                 f"<b>Status:</b> {row['status']}<br>" \
                 f"<b>Water Level:</b> {row['value']}"
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=folium.Popup(popup_text, max_width=200),
        color=get_color(row['status']),
        fill=True,
        fill_color=get_color(row['status']),
        fill_opacity=0.7
    ).add_to(m)

# 5. Сохранение результата
m.save("10.html")

print("Modeling complete. The map has been saved as 10.html")