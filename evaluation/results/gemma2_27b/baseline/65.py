import pandas as pd
import folium

# Загрузка данных с датчиков (пример)
data = pd.read_csv("water_level_data.csv") 

# Определение пороговых значений
threshold_aksu = 2.5  # Примерный порог для Aksu River
threshold_byzhy = 1.8 # Примерный порог для Byzhy River

# Проверка данных и выявление неисправных датчиков
problem_sensors = []
for index, row in data.iterrows():
    river = row['River']
    level = row['Level']
    if river == 'Aksu River':
        if level > threshold_aksu or level < 0:
            problem_sensors.append((row['SensorID'], 'Aksu River'))
    elif river == 'Byzhy River':
        if level > threshold_byzhy or level < 0:
            problem_sensors.append((row['SensorID'], 'Byzhy River'))

# Вывод списка потенциально неисправных датчиков
print("Потенциально неисправные датчики:")
for sensor, river in problem_sensors:
    print(f"Датчик {sensor} на реке {river}")

# Визуализация (необязательно)
m = folium.Map(location=[42.87, 74.59], zoom_start=10) # Примерные координаты

# Добавление маркеров датчиков на карту (пример)
for index, row in data.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=f"Датчик {row['SensorID']}").add_to(m)

# Сохранение карты
m.save("65.html")