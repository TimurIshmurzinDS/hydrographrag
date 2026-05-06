import folium
import pandas as pd
import random

# 1. Имитация данных гидрологических постов на реке Коктал
# В реальном проекте здесь будет запрос к API или загрузка файла .geojson / .csv
data = {
    'station_id': [101, 102, 103, 104, 105],
    'station_name': ['Верхний Коктал', 'Средний Коктал', 'Пост у поселка', 'Нижний Коктал', 'Устье Коктала'],
    'lat': [51.25, 51.10, 50.95, 50.80, 50.65],
    'lon': [86.10, 86.25, 86.40, 86.55, 86.70],
    'water_level': [1.2, 2.5, 4.8, 3.1, 1.5], # Текущий уровень в метрах
    'critical_level': [3.0, 3.0, 4.5, 3.0, 3.0] # Порог опасности
}

df = pd.DataFrame(data)

def get_status_color(current, critical):
    """Определяет цвет маркера в зависимости от уровня воды"""
    if current >= critical:
        return 'red'    # Опасность
    elif current >= critical * 0.7:
        return 'orange' # Внимание
    else:
        return 'green'  # Норма

def get_status_text(current, critical):
    """Определяет текстовый статус"""
    if current >= critical:
        return 'ОПАСНОСТЬ'
    elif current >= critical * 0.7:
        return 'ВНИМАНИЕ'
    else:
        return 'НОРМА'

# 2. Создание карты
# Центрируем карту на примерном расположении реки Коктал (Алтайский край/Республика Алтай)
m = folium.Map(location=[50.95, 86.40], zoom_start=8, tiles='OpenStreetMap')

# 3. Добавление постов на карту и формирование списка
stations_list = []

for index, row in df.iterrows():
    color = get_status_color(row['water_level'], row['critical_level'])
    status = get_status_text(row['water_level'], row['critical_level'])
    
    # Сохраняем данные для итогового списка
    stations_list.append({
        'Пост': row['station_name'],
        'Уровень': row['water_level'],
        'Статус': status
    })
    
    # Создаем всплывающее окно
    popup_text = f"<b>Пост:</b> {row['station_name']}<br>" \
                 f"<b>Уровень:</b> {row['water_level']} м<br>" \
                 f"<b>Статус:</b> {status}"
    
    # Добавляем маркер на карту
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# 4. Вывод списка в консоль (согласно требованию задачи)
print("Список постов на реке Koktal River и текущий уровень воды:")
print("-" * 50)
print(f"{'Название поста':<20} | {'Уровень (м)':<12} | {'Статус':<10}")
print("-" * 50)
for s in stations_list:
    print(f"{s['Пост']:<20} | {s['Уровень']:<12} | {s['Статус']:<10}")

# 5. Сохранение карты
m.save("88.html")