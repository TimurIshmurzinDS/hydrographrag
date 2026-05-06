import folium
import pandas as pd

# Загрузка данных о датчиках (замените на ваши данные)
sensors = pd.read_csv("sensors_data.csv")

# Создание карты
m = folium.Map(location=[sensors['latitude'].mean(), sensors['longitude'].mean()], zoom_start=12)

# Добавление маркеров датчиков на карту
for index, row in sensors.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Датчик {row['sensor_id']}"
    ).add_to(m)

# Сохранение карты
m.save("14.html")

# Дальнейший анализ временных рядов и расчет показателей работоспособности 
# (код зависит от формата ваших данных и целей анализа)