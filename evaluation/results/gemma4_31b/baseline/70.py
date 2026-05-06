import folium
import pandas as pd

# 1. Симуляция данных гидрологических постов на реке Шарын
# В реальном сценарии здесь будет загрузка из API или CSV/Database
data = {
    'station_id': [101, 102, 103, 104, 105],
    'station_name': ['Upper Sharyn', 'Middle Sharyn A', 'Middle Sharyn B', 'Lower Sharyn', 'Sharyn Delta'],
    'lat': [43.25, 43.10, 42.95, 42.70, 42.50],
    'lon': [79.10, 79.30, 79.60, 79.90, 80.20],
    'current_level': [1.2, 4.5, 2.1, 5.8, 3.0], # Текущий уровень в метрах
    'critical_threshold': [2.0, 4.0, 2.5, 5.0, 3.5] # Порог критического уровня
}

df = pd.DataFrame(data)

# 2. Определение критического статуса
def check_status(row):
    if row['current_level'] >= row['critical_threshold']:
        return 'Critical'
    return 'Normal'

df['status'] = df.apply(check_status, axis=1)

# 3. Идентификация постов с критическим уровнем
critical_posts = df[df['status'] == 'Critical']
print("Посты с критическим уровнем воды:")
print(critical_posts[['station_name', 'current_level', 'critical_threshold']])

# 4. Визуализация на карте
# Центрируем карту на примерном расположении реки Шарын
m = folium.Map(location=[42.8, 79.6], zoom_start=7, tiles='OpenStreetMap')

for index, row in df.iterrows():
    # Выбор цвета в зависимости от статуса
    color = 'red' if row['status'] == 'Critical' else 'green'
    
    # Создание текста для всплывающего окна
    popup_text = (
        f"Station: {row['station_name']}<br>"
        f"Current Level: {row['current_level']}m<br>"
        f"Threshold: {row['critical_threshold']}m<br>"
        f"Status: <b>{row['status']}</b>"
    )
    
    # Добавление маркера на карту
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# 5. Сохранение карты
m.save("70.html")
print("\nКарта успешно сохранена в файл 70.html")