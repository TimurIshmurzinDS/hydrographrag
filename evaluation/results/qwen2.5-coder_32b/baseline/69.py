import pandas as pd
import folium

# Предполагаем, что данные о датчиках представлены в формате CSV с колонками: 'river', 'sensor_id', 'latitude', 'longitude', 'status'
data = {
    'river': ['Koktal River', 'Koktal River', 'Aksu River', 'Aksu River'],
    'sensor_id': [1, 2, 3, 4],
    'latitude': [42.8500, 42.8600, 42.9000, 42.9100],
    'longitude': [78.2500, 78.2600, 78.3000, 78.3100],
    'status': ['active', 'inactive', 'active', 'active']
}

# Создание DataFrame
df = pd.DataFrame(data)

# Функция для определения цвета маркера на карте в зависимости от статуса датчика
def get_marker_color(status):
    if status == 'active':
        return 'green'
    else:
        return 'red'

# Создание карты с центром между реками Koktal и Aksu
m = folium.Map(location=[42.8750, 78.2750], zoom_start=11)

# Добавление маркеров на карту для каждого датчика
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Река: {row['river']}, Датчик ID: {row['sensor_id']}, Статус: {row['status']}",
        icon=folium.Icon(color=get_marker_color(row['status']))
    ).add_to(m)

# Сохранение карты в файл
m.save("69.html")