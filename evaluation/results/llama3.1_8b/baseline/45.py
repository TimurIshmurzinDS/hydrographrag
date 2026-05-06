# Импорт необходимых библиотек
import folium
import pandas as pd

# Загрузка данных о предприятиях в реке Кумбель
data = {
    'Название': ['Предприятие 1', 'Предприятие 2', 'Предприятие 3'],
    'Координаты': [[55.7558, 37.6173], [55.7559, 37.6184], [55.7560, 37.6195]],
    'Потребление воды (м³)': [100, 200, 300]
}

df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[55.7558, 37.6173], zoom_start=12)

# Добавление слоя для отображения предприятий в реке Кумбель
folium.Marker(
    location=df['Координаты'].iloc[0],
    popup='Предприятие 1',
    icon=folium.Icon(color='red')
).add_to(m)

folium.Marker(
    location=df['Координаты'].iloc[1],
    popup='Предприятие 2',
    icon=folium.Icon(color='green')
).add_to(m)

folium.Marker(
    location=df['Координаты'].iloc[2],
    popup='Предприятие 3',
    icon=folium.Icon(color='blue')
).add_to(m)

# Добавление слоя с данными о потреблении воды предприятиями
for i in range(len(df)):
    folium.Marker(
        location=df['Координаты'].iloc[i],
        popup=f'Потребление воды: {df["Потребление воды (м³)"].iloc[i]} м³',
        icon=folium.Icon(color='gray')
    ).add_to(m)

# Сохранение карты как HTML-файл
m.save("45.html")