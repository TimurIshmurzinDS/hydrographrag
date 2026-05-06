import pandas as pd
import folium

# Предполагаем, что у нас есть данные о гидропостах и их уровнях воды.
# Для примера создадим DataFrame с этими данными.

data = {
    'name': ['ГП1', 'ГП2', 'ГП3'],
    'latitude': [45.03, 45.06, 45.10],
    'longitude': [89.97, 90.01, 90.05],
    'water_level': [152.3, 153.1, 151.8]  # Уровни воды в метрах над уровнем моря
}

df = pd.DataFrame(data)

# Создание карты с центром на средних координатах гидропостов
map_center = [df['latitude'].mean(), df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Добавление маркеров на карту для каждого гидропоста с информацией о уровне воды
for index, row in df.iterrows():
    popup_text = f"Гидропост: {row['name']}\nУровень воды: {row['water_level']} м"
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text,
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("63.html")