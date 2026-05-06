import pandas as pd
import folium

# Пример данных: таблица с реками и их текущими уровнями воды
data = {
    'River': ['Дон', 'Волга', 'Камень', 'Суваля'],
    'Current_Level': [10, 25, 30, 40],
    'Critical_Level': [20, 25, 28, 35]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Определение критических уровней
df['Is_Critical'] = df['Current_Level'] > df['Critical_Level']

# Фильтрация данных для критических рек
critical_rivers = df[df['Is_Critical']]['River'].tolist()

# Создание карты
m = folium.Map(location=[50, 37], zoom_start=4)

# Добавление маркеров на карте для критических рек
for river in critical_rivers:
    # Пример координат для каждой реки (замените на реальные данные)
    if river == 'Дон':
        lat, lon = 45.0361, 42.8797
    elif river == 'Волга':
        lat, lon = 53.2231, 45.0361
    elif river == 'Камень':
        lat, lon = 55.7558, 37.6173
    elif river == 'Суваля':
        lat, lon = 59.9386, 30.3234
    
    folium.Marker([lat, lon], popup=f'{river} (Критический уровень)').add_to(m)

# Сохранение карты
m.save("141.html")