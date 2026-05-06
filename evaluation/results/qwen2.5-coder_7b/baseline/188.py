import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Пример данных (замените на реальные данные)
data_sharyn = {
    'Latitude': [51.23, 51.24],
    'Longitude': [76.45, 76.46],
    'WaterQuality': ['Good', 'Moderate'],
    'FishSpecies': ['Salmon', 'Trout']
}

data_urzhar = {
    'Latitude': [50.98, 51.00],
    'Longitude': [75.32, 75.34],
    'WaterQuality': ['Poor', 'Good'],
    'FishSpecies': ['Bream', 'Perch']
}

# Создание DataFrame для Шарына
df_sharyn = pd.DataFrame(data_sharyn)
df_sharyn['Status'] = df_sharyn['WaterQuality']

# Создание DataFrame для Уржара
df_urzhar = pd.DataFrame(data_urzhar)
df_urzhar['Status'] = df_urzhar['WaterQuality']

# Объединение данных
combined_data = pd.concat([df_sharyn, df_urzhar], ignore_index=True)

# Создание карты
m = folium.Map(location=[51.06, 75.89], zoom_start=6)

# Добавление маркеров на карте
marker_cluster = MarkerCluster().add_to(m)

for index, row in combined_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Река: {index + 1}\nКачество воды: {row['WaterQuality']}\nВиды рыб: {', '.join(row['FishSpecies'])}",
        icon=folium.Icon(color='red' if row['Status'] == 'Poor' else 'green')
    ).add_to(marker_cluster)

# Сохранение карты
m.save("188.html")