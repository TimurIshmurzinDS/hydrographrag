import folium
import pandas as pd

# Загрузка данных о предприятиях (предполагается, что данные находятся в CSV-файле)
data = pd.read_csv("enterprises.csv")

# Геокодирование адресов предприятий (используя Nominatim или другой сервис)
# ...

# Создание карты
m = folium.Map(location=[45.0, 40.0], zoom_start=10)  # Установить координаты центра карты

# Добавление точек на карту
for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Предприятие: {row['name']}<br>Тип деятельности: {row['type']}<br>Потребление воды: {row['water_consumption']} м3",
        icon=folium.Icon(color='blue')  # Цвет иконки может зависеть от типа деятельности
    ).add_to(m)

# Сохранение карты
m.save("45.html")