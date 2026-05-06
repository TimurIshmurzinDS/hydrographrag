import pandas as pd
import folium

# Загрузка данных (замените 'data.csv' на фактический путь к файлу)
data = pd.read_csv('data.csv')

# Создание карты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Добавление маркеров с информацией о расходе воды
for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Дата: {row['date']}<br>Расход: {row['flow']} м³/с",
    ).add_to(m)

# Сохранение карты
m.save("48.html")