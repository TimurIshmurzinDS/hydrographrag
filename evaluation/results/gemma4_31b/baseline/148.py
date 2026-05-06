import pandas as pd
import folium
from folium.plugins import MarkerCluster

# 1. Симуляция данных гидрологических замеров
# В реальном сценарии здесь будет запрос к API (например, Roshydromet или аналогичным)
data = {
    'river_name': ['Волга', 'Лена', 'Обь', 'Енисей', 'Амур', 'Дон', 'Нева', 'Иртыш'],
    'lat': [57.38, 62.03, 55.01, 56.44, 51.67, 47.22, 59.93, 54.87],
    'lon': [48.32, 129.73, 82.93, 92.85, 123.63, 39.51, 30.33, 68.65],
    'current_level': [4.2, 7.8, 3.1, 5.5, 8.2, 2.1, 1.5, 6.4], # Текущий уровень в метрах
    'threshold_level': [4.0, 6.0, 3.5, 5.0, 7.0, 2.5, 1.2, 5.0], # Пороговый уровень
    'critical_level': [5.0, 9.0, 4.5, 7.0, 10.0, 3.5, 2.0, 8.0] # Критический уровень
}

df = pd.DataFrame(data)

# 2. Анализ уровней воды
def determine_status(row):
    if row['current_level'] >= row['critical_level']:
        return 'Danger'
    elif row['current_level'] > row['threshold_level']:
        return 'Elevated'
    else:
        return 'Normal'

df['status'] = df.apply(determine_status, axis=1)

# Фильтруем только те реки, где уровень повышен или опасен
elevated_rivers = df[df['status'] != 'Normal'].copy()

# 3. Визуализация на карте
# Центрируем карту по средним координатам всех станций
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=3, tiles='CartoDB positron')

# Создаем кластеры для маркеров
marker_cluster = MarkerCluster().add_to(m)

# Цветовая схема для статусов
color_map = {
    'Elevated': 'orange',
    'Danger': 'red'
}

for index, row in elevated_rivers.iterrows():
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>Река:</b> {row['river_name']}<br>"
        f"<b>Статус:</b> {row['status']}<br>"
        f"<b>Текущий уровень:</b> {row['current_level']} м<br>"
        f"<b>Порог:</b> {row['threshold_level']} м"
    )
    
    # Добавляем маркер на карту
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_text,
        color=color_map[row['status']],
        fill=True,
        fill_color=color_map[row['status']],
        fill_opacity=0.7
    ).add_to(marker_cluster)

# 4. Сохранение результата
m.save("148.html")

print("Анализ завершен. Карта с повышенным уровнем воды сохранена в файл 148.html")
print(f"Обнаружено проблемных участков: {len(elevated_rivers)}")