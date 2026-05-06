python
import pandas as pd
import folium

# Загрузка данных из CSV файлов (заменить на ваши пути к файлам)
data_lepys = pd.read_csv("data_lepys.csv", index_col="datetime")
data_kishi_osek = pd.read_csv("data_kishi_osek.csv", index_col="datetime")

# Определение периодов отсутствия сигнала
missing_lepys = data_lepys[data_lepys["signal"] == 0].index
missing_kishi_osek = data_kishi_osek[data_kishi_osek["signal"] == 0].index

# Создание карты с Folium
m = folium.Map(location=[54.7, 61.3], zoom_start=12)

# Пометка датчиков на карте (заменить координаты на реальные)
folium.Marker([54.7, 61.3], popup="Датчик Лепсы").add_to(m)
folium.Marker([54.8, 61.2], popup="Датчик Киши Осек").add_to(m)

# Визуализация периодов отсутствия сигнала (заменить на реальные координаты датчиков)
for i in missing_lepys:
    folium.CircleMarker([54.7, 61.3], radius=5, color="red", fill=True).add_to(m)

for i in missing_kishi_osek:
    folium.CircleMarker([54.8, 61.2], radius=5, color="blue", fill=True).add_to(m)

# Сохранение карты
m.save("149.html")