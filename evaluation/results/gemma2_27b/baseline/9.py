import pandas as pd
import folium

# 1. Загрузка данных о уровнях воды (пример)
data = {
    'river': ['Ili', 'Karatal', 'Ili', 'Karatal'],
    'location': ['point_A', 'point_B', 'point_C', 'point_D'],
    'level': [12.5, 8.2, 13.1, 9.7]
}

df = pd.DataFrame(data)

# 2. Геопространственная привязка (пример координат)
coordinates = {
    'point_A': [43.0, 77.5],
    'point_B': [42.5, 76.0],
    'point_C': [43.2, 78.0],
    'point_D': [42.8, 75.5]
}

# 3. Создание карты
m = folium.Map(location=[43.0, 77.0], zoom_start=8)

# 4. Добавление маркеров с уровнями воды
for index, row in df.iterrows():
    folium.Marker(
        location=coordinates[row['location']],
        popup=f"Река: {row['river']}<br>Уровень: {row['level']} м",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# 5. Сохранение карты
m.save("9.html")