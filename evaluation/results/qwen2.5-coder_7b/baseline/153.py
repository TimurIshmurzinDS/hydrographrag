import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

# Пример данных: уровень воды в реках за год (в метрах)
data = {
    'River': ['Sarykan', 'Kara-Kol', 'Talas', 'Naryn'],
    'Winter': [10, 5, 8, 7],
    'Spring': [20, 15, 30, 25],
    'Summer': [15, 10, 25, 20],
    'Autumn': [12, 8, 20, 18]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Определение функции для оценки уровня подверженности весеннему половодью
def spring_flood_risk(row):
    return row['Spring'] - row['Winter']

# Применение функции к каждой строке DataFrame
df['Spring_Flood_Risk'] = df.apply(spring_flood_risk, axis=1)

# Сортировка по уровню подверженности весеннему половодью в порядке убывания
df_sorted = df.sort_values(by='Spring_Flood_Risk', ascending=False)

# Вывод результатов
print("Реки, наиболее подвержены весеннему половодью:")
print(df_sorted[['River', 'Spring_Flood_Risk']])

# Создание карты с использованием folium
m = folium.Map(location=[42.05, 76.98], zoom_start=6)

# Добавление маркеров на карте
marker_cluster = MarkerCluster().add_to(m)
for index, row in df_sorted.iterrows():
    folium.Marker(
        location=[42.05, 76.98],  # Пример координат (замените на реальные данные)
        popup=f"{row['River']} - Уровень подверженности весеннему половодью: {row['Spring_Flood_Risk']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(marker_cluster)

# Сохранение карты
m.save("153.html")