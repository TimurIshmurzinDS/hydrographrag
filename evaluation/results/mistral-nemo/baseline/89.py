import pandas as pd
import folium

# Загружаем данные о расходе воды на реке Baskan River и уровне реки Prokhodnaya River в период пика половодья
baskan_data = pd.read_csv('baskan_river_data.csv')
prokhodnaya_data = pd.read_csv('prokhodnaya_river_data.csv')

# Сопоставляем данные по времени
merged_data = pd.merge(baskan_data, prokhodnaya_data, on='time', how='inner')

# Вычисляем разницу между уровнями воды на двух реках
merged_data['difference'] = merged_data['baskan_level'] - merged_data['prokhodnaya_level']

# Создаем карту с помощью библиотеки folium и добавляем на нее точки с данными о расходе воды
m = folium.Map(location=[50, 100], zoom_start=4)

for index, row in merged_data.iterrows():
    folium.CircleMarker(
        location=[row['baskan_lat'], row['baskan_lon']],
        radius=row['difference']/10,
        color='blue',
        fill=True
    ).add_to(m)

# Сохраняем карту в файл HTML
m.save("89.html")