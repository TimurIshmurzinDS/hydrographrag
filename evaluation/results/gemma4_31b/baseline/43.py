import folium
import pandas as pd

# 1. Имитация данных по оросительным зонам вдоль реки Аягоз
# В реальном сценарии эти данные загружаются из GeoJSON или Shapefile
data = {
    'zone_id': [1, 2, 3, 4, 5],
    'name': ['Северный узел', 'Центральный-1', 'Центральный-2', 'Южный узел', 'Нижний узел'],
    'lat': [49.85, 49.70, 49.55, 49.40, 49.25],
    'lon': [82.10, 82.20, 82.35, 82.40, 82.50],
    'area_ha': [1200, 2500, 1800, 3000, 1500],  # Площадь в гектарах
    'water_norm_m3_ha': [450, 500, 480, 520, 460] # Норма полива м3 на 1 га
}

df = pd.DataFrame(data)

# 2. Расчет объема воды для каждой зоны и общего объема
df['volume_m3'] = df['area_ha'] * df['water_norm_m3_ha']
total_volume = df['volume_m3'].sum()

print(f"Расчетный объем воды, выделяемый на орошение: {total_volume:,} м³")

# 3. Создание карты
# Центр карты в районе реки Аягоз (Казахстан)
m = folium.Map(location=[49.5, 82.3], zoom_start=8, tiles='OpenStreetMap')

# Имитация русла реки (линия)
river_coords = [
    [49.90, 82.00], [49.85, 82.10], [49.70, 82.20], 
    [49.55, 82.35], [49.40, 82.40], [49.20, 82.60]
]
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Река Аягоз").add_to(m)

# Добавление зон орошения на карту
for index, row in df.iterrows():
    # Цвет круга зависит от объема воды (чем больше, тем интенсивнее красный)
    color = 'orange' if row['volume_m3'] < 1000000 else 'red'
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['area_ha'] / 200, # Радиус пропорционален площади
        popup=f"Зона: {row['name']}<br>Площадь: {row['area_ha']} га<br>Объем: {row['volume_m3']:,} м³",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6
    ).add_to(m)

# Добавление текстовой метки с общим итогом
folium.Marker(
    location=[49.5, 82.3],
    icon=folium.Icon(color='green', icon='info-sign'),
    popup=f"Общий объем выделяемой воды: {total_volume:,} м³"
).add_to(m)

# Сохранение карты
m.save("43.html")

print("Карта успешно сохранена в файл 43.html")