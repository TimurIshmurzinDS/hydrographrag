import folium
import pandas as pd

# Загружаем данные о высоте воды в реках
data = {
    'river': ['Karaoy River', 'Temirlik River', 'Turgen River'],
    'water_level': [10.5, 9.8, 12.3],
}

df = pd.DataFrame(data)

# Пороговые значения для опасного роста уровня воды
threshold = 11

# Определяем реки с опасным ростом уровня воды
df['dangerous_rise'] = df['water_level'] > threshold

# Координаты рек (для примера, могут быть получены из других источников)
coordinates = {
    'Karaoy River': [43.26, 76.90],
    'Temirlik River': [41.85, 69.24],
    'Turgen River': [43.28, 77.02],
}

# Создаем карту с помощью folium
m = folium.Map(location=[42.5, 70], zoom_start=8)

# Добавляем реки на карту и отмечаем те, у которых есть опасный рост уровня воды
for river in df['river']:
    coord = coordinates[river]
    if df[df['river'] == river]['dangerous_rise'].iloc[0]:
        folium.Marker(coord, popup=f"{river}: Опасный рост уровня воды", icon=folium.Icon(color='red')).add_to(m)
    else:
        folium.Marker(coord, popup=f"{river}: Уровень воды в норме", icon=folium.Icon(color='green')).add_to(m)

# Сохраняем карту как HTML-файл
m.save("86.html")