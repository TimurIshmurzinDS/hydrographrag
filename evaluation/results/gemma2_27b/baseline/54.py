import pandas as pd
import folium

# Загрузка данных о расходе воды (замените на фактический путь к файлу)
data = pd.read_csv("karkara_water_flow.csv")

# Преобразование даты в формат datetime
data['date'] = pd.to_datetime(data['date'])

# Разделение данных по десятилетиям
recent_decade = data[data['date'].dt.year >= 2010]
previous_decade = data[data['date'].dt.year < 2010]

# Расчет среднего расхода воды
recent_average = recent_decade['flow'].mean()
previous_average = previous_decade['flow'].mean()

# Вычисление разницы
difference = recent_average - previous_average

print(f"Разница в среднем расходе воды между последним и предыдущим десятилетиями: {difference:.2f}")

# Визуализация (необязательно)
m = folium.Map(location=[41.58, 69.20], zoom_start=8)  # Замените на координаты реки Karkara

# Добавление данных о расходе воды на карту (пример)
folium.Marker([41.58, 69.20], popup=f"Разница: {difference:.2f}").add_to(m)

m.save("54.html")