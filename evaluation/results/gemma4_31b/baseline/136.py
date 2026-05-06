import folium
import pandas as pd
import random

# 1. Симуляция данных датчиков уровня воды
# В реальном сценарии здесь будет загрузка из БД или API (например, pd.read_csv или requests.get)
data = {
    'sensor_id': [f'SN_{i}' for i in range(1, 11)],
    'name': [f'Датчик {i}' for i in range(1, 11)],
    'lat': [55.75 + random.uniform(-0.5, 0.5) for _ in range(10)],
    'lon': [37.61 + random.uniform(-0.5, 0.5) for _ in range(10)],
    'status': random.choices(['Active', 'Warning', 'Offline'], k=10),
    'water_level': [round(random.uniform(1.2, 5.8), 2) for _ in range(10)]
}

df = pd.DataFrame(data)

# 2. Функция для определения цвета маркера в зависимости от статуса
def get_color(status):
    if status == 'Active':
        return 'green'
    elif status == 'Warning':
        return 'orange'
    elif status == 'Offline':
        return 'red'
    else:
        return 'gray'

# 3. Создание карты
# Центрируем карту по средним координатам датчиков
center_lat = df['lat'].mean()
center_lon = df['lon'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles='OpenStreetMap')

# 4. Добавление датчиков на карту
for index, row in df.iterrows():
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>ID:</b> {row['sensor_id']}<br>"
        f"<b>Название:</b> {row['name']}<br>"
        f"<b>Статус:</b> {row['status']}<br>"
        f"<b>Уровень воды:</b> {row['water_level']} м."
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_text,
        color=get_color(row['status']),
        fill=True,
        fill_color=get_color(row['status']),
        fill_opacity=0.7
    ).add_to(m)

# 5. Сохранение карты
m.save("136.html")

print("Анализ завершен. Карта с итоговым статусом датчиков сохранена в файл '136.html'.")

# Вывод краткого отчета в консоль
print("\n--- Отчет по статусам датчиков ---")
print(df['status'].value_counts())