import folium
import pandas as pd

# 1. Имитация данных мониторинга основных рек
# В реальном сценарии здесь будет запрос к API (например, через requests)
data = {
    'river_name': ['Волга', 'Дон', 'Обь', 'Енисей', 'Лена', 'Амур', 'Нева', 'Урал'],
    'lat': [57.3, 47.2, 55.0, 56.4, 62.1, 52.5, 59.9, 52.2],
    'lon': [48.3, 39.1, 82.9, 92.8, 129.7, 128.5, 30.3, 53.5],
    'current_level': [5.2, 2.1, 7.8, 4.1, 8.5, 6.2, 1.5, 4.8], # Текущий уровень в метрах
    'critical_level': [5.0, 3.0, 7.0, 5.0, 8.0, 6.0, 2.0, 4.5] # Критический порог в метрах
}

df = pd.DataFrame(data)

# 2. Анализ уровней воды
# Определяем, является ли уровень критическим
df['is_critical'] = df['current_level'] >= df['critical_level']
df['diff'] = df['current_level'] - df['critical_level']

# 3. Создание карты
# Центрируем карту по средним координатам
m = folium.Map(location=[58, 60], zoom_start=3, tiles='CartoDB positron')

# 4. Добавление объектов на карту
for index, row in df.iterrows():
    # Определяем цвет маркера в зависимости от статуса
    color = 'red' if row['is_critical'] else 'green'
    status = 'КРИТИЧЕСКИЙ' if row['is_critical'] else 'Норма'
    
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>Река:</b> {row['river_name']}<br>"
        f"<b>Статус:</b> {status}<br>"
        f"<b>Текущий уровень:</b> {row['current_level']} м<br>"
        f"<b>Критический уровень:</b> {row['critical_level']} м<br>"
        f"<b>Отклонение:</b> {row['diff']:.2f} м"
    )
    
    # Добавляем круглый маркер
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# 5. Сохранение результата
m.save("141.html")

print("Анализ завершен. Карта с критическими уровнями воды сохранена в файл 141.html")

# Вывод списка критических рек в консоль для проверки
critical_rivers = df[df['is_critical']]['river_name'].tolist()
print(f"Критические уровни обнаружены на следующих реках: {', '.join(critical_rivers)}")