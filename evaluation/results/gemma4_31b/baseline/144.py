import folium
import pandas as pd
import random

def solve_water_level_monitoring():
    # 1. Имитация данных датчиков в бассейне реки Или
    # В реальном сценарии здесь будет запрос к API (например, через requests)
    sensors_data = [
        {"id": "S1", "name": "Верхний Или", "lat": 43.2, "lon": 80.1, "level": 4.2, "threshold": 5.0},
        {"id": "S2", "name": "Средний Или", "lat": 43.5, "lon": 79.5, "level": 5.8, "threshold": 5.5}, # Alert!
        {"id": "S3", "name": "Нижний Или", "lat": 43.8, "lon": 78.2, "level": 3.1, "threshold": 5.0},
        {"id": "S4", "name": "Приток Текели", "lat": 43.1, "lon": 78.5, "level": 6.1, "threshold": 4.5}, # Alert!
        {"id": "S5", "name": "Район озера Балхаш", "lat": 43.9, "lon": 77.1, "level": 2.5, "threshold": 5.0},
    ]

    # Преобразование в DataFrame для удобства анализа
    df = pd.DataFrame(sensors_data)

    # 2. Логика определения оповещений
    def check_status(row):
        if row['level'] > row['threshold']:
            return 'Danger', 'red'
        elif row['level'] > row['threshold'] * 0.8:
            return 'Warning', 'orange'
        else:
            return 'Normal', 'green'

    # Применяем функцию для определения статуса и цвета
    df[['status', 'color']] = df.apply(
        lambda row: pd.Series(check_status(row)), axis=1
    )

    # 3. Поиск датчиков с оповещениями
    alerts = df[df['status'] != 'Normal']
    
    print(f"Обнаружено оповещений: {len(alerts)}")
    for index, row in alerts.iterrows():
        print(f"Оповещение: Датчик {row['name']} - Статус: {row['status']} (Уровень: {row['level']}, Порог: {row['threshold']})")

    # 4. Визуализация на карте
    # Центрируем карту на бассейне реки Или
    m = folium.Map(location=[43.5, 78.5], zoom_start=7, tiles='CartoDB positron')

    for _, row in df.iterrows():
        # Создаем текст для всплывающего окна
        popup_text = (
            f"<b>Датчик:</b> {row['name']}<br>"
            f"<b>Статус:</b> {row['status']}<br>"
            f"<b>Уровень:</b> {row['level']} м.<br>"
            f"<b>Порог:</b> {row['threshold']} м."
        )
        
        # Добавляем маркер на карту
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            popup=popup_text,
            color=row['color'],
            fill=True,
            fill_color=row['color'],
            fill_opacity=0.7
        ).add_to(m)

    # Сохранение карты
    m.save("144.html")
    print("\nКарта сохранена в файл 144.html")

if __name__ == "__main__":
    solve_water_level_monitoring()