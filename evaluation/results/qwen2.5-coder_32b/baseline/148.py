import pandas as pd
import folium

# Пример данных о текущих уровнях воды в реках (в реальности данные должны быть получены из надежного источника)
data = {
    'river_name': ['Река Волга', 'Река Днепр', 'Река Обь', 'Река Енисей'],
    'current_water_level': [150, 230, 80, 95],
    'normal_water_level': [140, 220, 75, 90]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Определение рек с повышенным уровнем воды
threshold = 1.1  # Порог для определения повышенного уровня воды (например, на 10% выше нормы)
df['is_high_water'] = df['current_water_level'] > df['normal_water_level'] * threshold

# Фильтрация рек с повышенным уровнем воды
high_water_rivers = df[df['is_high_water']]

# Координаты для примера (в реальности должны быть получены из данных о местоположении рек)
coordinates = {
    'Река Волга': [56.1290, 47.3831],
    'Река Днепр': [48.3830, 35.0458],
    'Река Обь': [53.9000, 87.0649],
    'Река Енисей': [56.1290, 92.8571]
}

# Создание карты
m = folium.Map(location=[55.7558, 37.6173], zoom_start=4)  # Карта России

# Добавление маркеров для рек с повышенным уровнем воды
for index, row in high_water_rivers.iterrows():
    river_name = row['river_name']
    current_level = row['current_water_level']
    normal_level = row['normal_water_level']
    lat, lon = coordinates[river_name]
    
    popup_text = f"Река: {river_name}<br>Текущий уровень воды: {current_level} м<br>Нормальный уровень воды: {normal_level} м"
    folium.Marker([lat, lon], popup=popup_text, icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("148.html")