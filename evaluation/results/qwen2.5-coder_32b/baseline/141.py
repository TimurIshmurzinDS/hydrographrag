import pandas as pd
import folium

# Пример данных о текущих уровнях воды на реках (в реальном приложении данные будут загружаться из внешнего источника)
data = {
    'river': ['Волга', 'Днепр', 'Урал', 'Обь'],
    'current_level': [120, 85, 60, 90],
    'critical_level': [130, 90, 70, 100]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Определение рек с критическими уровнями воды
critical_rivers = df[df['current_level'] > df['critical_level']]

# Координаты основных рек (примерные значения)
coordinates = {
    'Волга': [54.1960, 45.2672],
    'Днепр': [48.3830, 35.0458],
    'Урал': [54.7833, 60.5833],
    'Обь': [61.9774, 73.8742]
}

# Создание карты
m = folium.Map(location=[55.7558, 37.6173], zoom_start=4)

# Добавление маркеров для рек с критическими уровнями воды
for index, row in critical_rivers.iterrows():
    river_name = row['river']
    current_level = row['current_level']
    critical_level = row['critical_level']
    lat, lon = coordinates[river_name]
    
    folium.Marker(
        location=[lat, lon],
        popup=f"Река: {river_name}<br>Текущий уровень: {current_level} м<br>Критический уровень: {critical_level} м",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("141.html")