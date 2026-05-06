import folium
import pandas as pd
import numpy as np
from geopy.distance import geodesic

# 1. Синтетические данные: Координаты русла реки Каратал (упрощенно)
# Река Каратал протекает в Казахстане
karatal_river_coords = [
    [43.20, 78.50], [43.25, 78.70], [43.30, 78.90], 
    [43.35, 79.10], [43.40, 79.30], [43.45, 79.50]
]

# 2. Данные по поселениям и рецептам
# Сравнение: Исторический состав (при реке) vs Современный состав
data = {
    'village': ['Village A', 'Village B', 'Village C', 'Village D', 'Village E'],
    'lat': [43.22, 43.28, 43.32, 43.42, 43.48],
    'lon': [78.55, 78.85, 79.05, 79.25, 79.60],
    'old_recipe': [
        'Полба, речная вода, дикие травы', 
        'Пшеница (местная), мед, соль', 
        'Ячмень, вода, семена льна', 
        'Пшеница, закваска, местный жир', 
        'Просо, вода, коренья'
    ],
    'new_recipe': [
        'Пшеничная мука в/с, дрожжи, сахар', 
        'Пшеничная мука, дрожжи, соль', 
        'Пшеничная мука, маргарин, сахар', 
        'Пшеничная мука, дрожжи, соль', 
        'Пшеничная мука, сахар, дрожжи'
    ]
}

df = pd.DataFrame(data)

# Функция для расчета минимального расстояния до реки
def calculate_min_distance(point, river_line):
    distances = [geodesic(point, river_pt).km for river_pt in river_line]
    return min(distances)

# Расчет расстояния для каждого поселения
river_points = [tuple(coord) for coord in karatal_river_coords]
df['dist_to_river'] = df.apply(lambda row: calculate_min_distance((row['lat'], row['lon']), river_points), axis=1)

# Определение степени изменения (упрощенно: если расстояние < 15км, влияние реки было значительным)
df['influence'] = df['dist_to_river'].apply(lambda x: 'High' if x < 15 else 'Low')

# 3. Визуализация на карте
m = folium.Map(location=[43.32, 79.00], zoom_start=8, tiles='CartoDB positron')

# Отрисовка реки Каратал
folium.PolyLine(karatal_river_coords, color="blue", weight=4, opacity=0.8, tooltip="Karatal River").add_to(m)

# Добавление поселений на карту
for index, row in df.iterrows():
    # Цвет маркера зависит от влияния реки
    color = 'green' if row['influence'] == 'High' else 'orange'
    
    popup_text = (
        f"<b>Village:</b> {row['village']}<br>"
        f"<b>Distance to River:</b> {row['dist_to_river']:.2f} km<br>"
        f"<b>Historical Recipe:</b> {row['old_recipe']}<br>"
        f"<b>Modern Recipe:</b> {row['new_recipe']}<br>"
        f"<b>Influence:</b> {row['influence']}"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

# Сохранение карты
m.save("273.html")

print("Modeling complete. The map has been saved as 273.html")