import folium
import pandas as pd

# Пример данных о текущем состоянии реки (замените на реальные данные)
data = {
    'latitude': [43.21, 43.22, 43.23],  # Широта точек мониторинга
    'longitude': [76.54, 76.55, 76.56],  # Долгота точек мониторинга
    'water_level': [100, 102, 98]  # Уровень воды в метрах
}

# Создаем DataFrame из данных
df = pd.DataFrame(data)

# Создаем карту
m = folium.Map(location=[43.22, 76.55], zoom_start=13)

# Добавляем маркеры с уровнями воды
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='red' if row['water_level'] > 100 else 'green')
    ).add_to(m)

# Сохраняем карту
m.save("16.html")