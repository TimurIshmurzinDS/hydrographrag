import pandas as pd
import folium

# Пример данных: DataFrame с информацией о реках, их текущих уровнях воды и нормальных значениях
data = {
    'River': ['Река А', 'Река Б', 'Река В'],
    'Current_Level': [10.5, 8.2, 9.7],
    'Normal_Level': [10.0, 8.0, 9.5]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Определение повышенных уровней воды
df['High_Water'] = df['Current_Level'] > df['Normal_Level']

# Фильтрация рек с повышенными уровнями воды
high_water_rivers = df[df['High_Water']]['River'].tolist()

# Создание карты
m = folium.Map(location=[50, 30], zoom_start=6)

# Добавление маркеров для рек с повышенными уровнями воды
for river in high_water_rivers:
    # Пример координат для каждой речи (замените на реальные данные)
    lat, lon = 51.5074, -0.1278  # Координаты Лондона для примера
    
    folium.Marker([lat, lon], popup=f'{river} имеет повышенный уровень воды', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("148.html")