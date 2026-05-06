import pandas as pd
import folium

# Шаг 1: Сбор данных
data = pd.read_csv('ili_river_data.csv') # Предполагается, что данные находятся в CSV-файле с названием 'ili_river_data.csv'

# Шаг 2: Очистка данных
data = data.dropna() # Удаление записей с пропущенными значениями

# Шаг 3: Анализ данных
# Предполагается, что данные содержат столбцы 'latitude', 'longitude' и 'water_level'
current_water_level = data['water_level'].max()

# Шаг 4: Моделирование
# Для этого примера мы просто берем максимальный уровень воды из данных,
# но в реальной ситуации здесь могло бы быть более сложное моделирование

# Шаг 5: Визуализация
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for i in range(len(data)):
    folium.CircleMarker(
        location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

folium.Marker([data['latitude'].mean(), data['longitude'].mean()], popup=f'Текущий уровень воды: {current_water_level} м').add_to(m)

m.save("1.html")