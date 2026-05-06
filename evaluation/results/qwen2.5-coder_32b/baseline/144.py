import pandas as pd
import folium

# Предполагаемый формат данных: CSV-файл с колонками 'latitude', 'longitude' и 'alert'
data = pd.read_csv('water_level_sensors.csv')

# Проверка наличия оповещений
data['has_alert'] = data['alert'].apply(lambda x: True if x == 1 else False)

# Создание карты с центром в районе реки Или (координаты примерные)
m = folium.Map(location=[42.035, 21.78], zoom_start=9)

# Добавление маркеров на карту
for index, row in data.iterrows():
    if row['has_alert']:
        icon_color = 'red'
        popup_text = "Оповещение!"
    else:
        icon_color = 'green'
        popup_text = "Нет оповещений"
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text,
        icon=folium.Icon(color=icon_color)
    ).add_to(m)

# Сохранение карты в файл
m.save("144.html")