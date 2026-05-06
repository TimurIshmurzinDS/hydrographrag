import folium
import pandas as pd

# 1. Имитация данных гидрологических постов
# В реальном сценарии здесь был бы запрос к API гидромета или загрузка CSV/Shapefile
data = {
    'station_id': [101, 102, 201, 202],
    'river': ['Sarykan River', 'Sarykan River', 'Aksu River', 'Aksu River'],
    'lat': [43.25, 43.10, 43.40, 43.20],
    'lon': [78.10, 78.25, 78.50, 78.65],
    'current_level': [1.2, 0.8, 2.5, 1.1],  # Текущий уровень в метрах
}

# Пороговое значение для орошения (например, 1.0 метр)
IRRIGATION_THRESHOLD = 1.0

df = pd.DataFrame(data)

# 2. Функция для определения статуса и цвета
def check_water_sufficiency(level):
    if level >= IRRIGATION_THRESHOLD + 0.5:
        return 'Достаточно', 'green'
    elif level >= IRRIGATION_THRESHOLD:
        return 'Пограничное состояние', 'orange'
    else:
        return 'Недостаточно', 'red'

# Применяем анализ
df[['status', 'color']] = df['current_level'].apply(
    lambda x: pd.Series(check_water_sufficiency(x))
)

# 3. Создание карты
# Центрируем карту в районе рек (примерные координаты Центральной Азии)
m = folium.Map(location=[43.25, 78.30], zoom_start=8, tiles='OpenStreetMap')

# Имитация геометрии рек (линии между постами)
rivers_coords = {
    'Sarykan River': [[43.25, 78.10], [43.10, 78.25]],
    'Aksu River': [[43.40, 78.50], [43.20, 78.65]]
}

for river_name, coords in rivers_coords.items():
    folium.PolyLine(coords, color="blue", weight=4, opacity=0.7, tooltip=river_name).add_to(m)

# Добавление маркеров гидропостов
for index, row in df.iterrows():
    status, color = check_water_sufficiency(row['current_level'])
    
    popup_text = (
        f"Река: {row['river']}<br>"
        f"Уровень: {row['current_level']} м<br>"
        f"Порог: {IRRIGATION_THRESHOLD} м<br>"
        f"<b>Статус: {status}</b>"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("106.html")

print("Анализ завершен. Результаты сохранены в файл 106.html")

# Вывод краткого отчета в консоль
for river in df['river'].unique():
    river_avg = df[df['river'] == river]['current_level'].mean()
    status = "Достаточно" if river_avg >= IRRIGATION_THRESHOLD else "Недостаточно"
    print(f"Река {river}: Средний уровень {river_avg:.2f}м -> {status}")