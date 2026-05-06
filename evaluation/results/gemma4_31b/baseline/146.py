import pandas as pd
import folium

# 1. Создание синтетического набора данных датчиков
# Координаты примерно соответствуют региону Восточного Казахстана
data = {
    'sensor_id': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'river': ['Аягоз', 'Аягоз', 'Аягоз', 'Токыраун', 'Токыраун', 'Токыраун'],
    'lat': [49.85, 49.92, 50.01, 49.70, 49.78, 49.88],
    'lon': [82.10, 82.25, 82.40, 82.00, 82.15, 82.30],
    'battery_level': [85, 15, 90, 10, 70, 50], # %
    'days_since_last_ping': [1, 5, 0, 10, 1, 2] # дни
}

df = pd.DataFrame(data)

# 2. Функция для определения необходимости ТО
def check_maintenance(row):
    if row['battery_level'] < 20 or row['days_since_last_ping'] > 3:
        return "Требуется ТО"
    return "Исправен"

# Применяем логику анализа
df['status'] = df.apply(check_maintenance, axis=1)

# 3. Визуализация на карте
# Центрируем карту в районе рек Аягоз и Токыраун
m = folium.Map(location=[49.85, 82.20], zoom_start=8, tiles='OpenStreetMap')

# Цветовая схема: Красный для ТО, Зеленый для нормы
def get_color(status):
    return 'red' if status == "Требуется ТО" else 'green'

# Добавление маркеров на карту
for index, row in df.iterrows():
    popup_text = (
        f"Датчик: {row['sensor_id']}<br>"
        f"Река: {row['river']}<br>"
        f"Заряд: {row['battery_level']}%<br>"
        f"Дней молчания: {row['days_since_last_ping']}<br>"
        f"<b>Статус: {row['status']}</b>"
    )
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color=get_color(row['status']), icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("146.html")

# Вывод результата в консоль для проверки
print("Анализ завершен. Результаты:")
print(df[['sensor_id', 'river', 'status']])
print("\nКарта сохранена в файл 146.html")