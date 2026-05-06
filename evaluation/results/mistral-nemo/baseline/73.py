import folium
import pandas as pd

# Загрузите данные о местоположении датчиков и их состоянии из источника данных
data = pd.read_csv('sensor_data.csv')

# Создайте географическую проекцию
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=5)

# Установите цвета отображения в зависимости от состояния датчика
colors = {
    'normal': '#00FF00',  # Зеленый - нормальный уровень воды
    'medium': '#FFFF00',  # Желтый - средний уровень воды
    'high': '#FF0000'     # Красный - высокий уровень воды
}

# Отобразите местоположение датчиков на карте с использованием библиотеки `folium`
for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color=colors[row['status']],
        fill=True
    ).add_to(m)

# Сохраните финальную карту как "73.html"
m.save("73.html")