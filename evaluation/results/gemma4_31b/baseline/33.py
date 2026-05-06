import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import LineString, Point

# 1. Создание синтетических данных (имитация реальных GIS-данных)
# Координаты реки Аксу (приблизительный маршрут)
river_coords = [
    (43.5, 81.0), (43.6, 81.2), (43.7, 81.5), 
    (43.8, 81.8), (43.9, 82.1), (44.0, 82.4)
]

# Данные по водозаборам для сельского хозяйства (названия, координаты, объем в млн м3/год)
intake_data = {
    'point_name': ['Водозабор Северный', 'Канал Восточный', 'Ирригационный узел А', 'Фермерский забор Б'],
    'lat': [43.55, 43.68, 43.82, 43.95],
    'lon': [81.1, 81.4, 81.7, 82.2],
    'volume_m3': [15.5, 22.1, 18.4, 12.0]  # Объем в млн м3
}

df_intakes = pd.DataFrame(intake_data)

# 2. Геопространственная обработка
# Создаем геометрию для реки
river_line = LineString(river_coords)

# Создаем GeoDataFrame для точек водозабора
geometry = [Point(xy) for xy in zip(df_intakes.lon, df_intakes.lat)]
gdf_intakes = gpd.GeoDataFrame(df_intakes, geometry=geometry, crs="EPSG:4326")

# 3. Расчет общего объема забора воды
total_volume = df_intakes['volume_m3'].sum()
print(f"Общий объем воды, забираемый на нужды сельского хозяйства: {total_volume:.2f} млн м3/год")

# 4. Визуализация с помощью folium
# Центр карты (среднее значение координат)
map_center = [43.75, 81.7]
m = folium.Map(location=map_center, zoom_start=7, tiles='OpenStreetMap')

# Добавление русла реки на карту
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.7, tooltip="Река Аксу").add_to(m)

# Добавление точек водозабора
for idx, row in df_intakes.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['volume_m3'] * 0.5, # Размер круга зависит от объема
        color='green',
        fill=True,
        fill_color='lime',
        popup=f"Объект: {row['point_name']}<br>Объем: {row['volume_m3']} млн м3/год"
    ).add_to(m)

# Добавление текстовой метки с итоговым результатом
folium.Marker(
    location=map_center,
    icon=folium.DivIcon(html=f"""<div style="font-family: Arial; color: black; font-weight: bold; 
                                background: white; padding: 10px; border: 2px solid blue; border-radius: 5px;">
                                Итоговый объем забора: {total_volume:.2f} млн м3/год</div>""")
).add_to(m)

# Сохранение карты
m.save("33.html")
print("Карта успешно сохранена в файл 33.html")