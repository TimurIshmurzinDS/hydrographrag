import folium
import pandas as pd

# 1. Подготовка данных (имитация данных с датчиков)
# В реальном сценарии здесь был бы запрос к API гидрологической службы
data = {
    'sensor_id': ['OS-01', 'OS-02', 'KT-01', 'KT-02', 'KT-03'],
    'river': ['Osek River', 'Osek River', 'Koktal River', 'Koktal River', 'Koktal River'],
    'lat': [42.5123, 42.5567, 42.6101, 42.6450, 42.6892],
    'lon': [75.1234, 75.1890, 75.3120, 75.3560, 75.4100],
    'status': ['Active', 'Inactive', 'Active', 'Active', 'Active'],
    'water_level': [2.1, 0.0, 4.8, 5.2, 1.9], # уровень в метрах
}

df = pd.DataFrame(data)

# Порог критического уровня воды
CRITICAL_LEVEL = 5.0

def get_sensor_color(row):
    """Определяет цвет маркера в зависимости от состояния датчика"""
    if row['status'] == 'Inactive':
        return 'red'  # Датчик не работает
    elif row['water_level'] > CRITICAL_LEVEL:
        return 'orange' # Критический уровень воды
    else:
        return 'green' # Все в норме

# 2. Создание карты
# Центрируем карту по средним координатам датчиков
map_center = [df['lat'].mean(), df['lon'].mean()]
m = folium.Map(location=map_center, zoom_start=11, tiles='OpenStreetMap')

# 3. Добавление датчиков на карту
for index, row in df.iterrows():
    color = get_sensor_color(row)
    
    # Формирование текста для всплывающего окна
    status_text = "OK" if color == 'green' else "ALERT"
    popup_info = (
        f"<b>Sensor ID:</b> {row['sensor_id']}<br>"
        f"<b>River:</b> {row['river']}<br>"
        f"<b>Status:</b> {row['status']}<br>"
        f"<b>Water Level:</b> {row['water_level']}m<br>"
        f"<b>Condition:</b> {status_text}"
    )
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_info, max_width=300),
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# 4. Сохранение результата
m.save("73.html")

print("Моделирование завершено. Карта сохранена в файл 73.html")