import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import LineString, Polygon

# 1. Создание синтетических данных для демонстрации (так как реальные Shape-файлы отсутствуют)
# Координаты примерно соответствуют региону Казахстана (Kurty, Lepsy)
rivers_data = {
    'name': ['Kurty River', 'Lepsy River'],
    'geometry': [
        LineString([(77.1, 43.5), (77.3, 43.6), (77.5, 43.7)]), # Упрощенная линия Kurty
        LineString([(77.6, 43.4), (77.8, 43.5), (78.0, 43.6)]), # Упрощенная линия Lepsy
    ],
    'annual_flow_m3': [150_000_000, 200_000_000] # Объем воды в м3 за год
}

agri_fields_data = {
    'field_id': [1, 2, 3],
    'crop_type': ['Wheat', 'Corn', 'Vegetables'],
    'area_ha': [5000, 3000, 2000],
    'water_demand_m3_per_ha': [4000, 7000, 9000], # Потребность в м3 на 1 га
    'geometry': [
        Polygon([(77.2, 43.5), (77.4, 43.5), (77.4, 43.6), (77.2, 43.6)]),
        Polygon([(77.7, 43.4), (77.9, 43.4), (77.9, 43.5), (77.7, 43.5)]),
        Polygon([(77.5, 43.6), (77.6, 43.6), (77.6, 43.7), (77.5, 43.7)]),
    ]
}

# Создание GeoDataFrames
gdf_rivers = gpd.GeoDataFrame(rivers_data, crs="EPSG:4326")
gdf_fields = gpd.GeoDataFrame(agri_fields_data, crs="EPSG:4326")

# 2. Расчет общего предложения воды (Supply)
total_supply = gdf_rivers['annual_flow_m3'].sum()

# 3. Расчет общего спроса на воду (Demand)
gdf_fields['total_field_demand'] = gdf_fields['area_ha'] * gdf_fields['water_demand_m3_per_ha']
total_demand = gdf_fields['total_field_demand'].sum()

# 4. Анализ достаточности
balance = total_supply - total_demand
is_sufficient = balance >= 0
status = "Достаточно" if is_sufficient else "Недостаточно"

print(f"Общий объем предложения: {total_supply:,} м3")
print(f"Общий объем спроса: {total_demand:,} м3")
print(f"Баланс: {balance:,} м3")
print(f"Результат: {status}")

# 5. Визуализация с помощью folium
m = folium.Map(location=[43.5, 77.5], zoom_start=9, tiles='CartoDB positron')

# Добавление рек на карту
for idx, row in gdf_rivers.iterrows():
    coords = [(p[1], p[0]) for p in row['geometry'].coords]
    folium.PolyLine(coords, color='blue', weight=4, opacity=0.8, 
                    popup=f"{row['name']} (Flow: {row['annual_flow_m3']:,} m3)").add_to(m)

# Добавление полей на карту
for idx, row in gdf_fields.iterrows():
    coords = [(p[1], p[0]) for p in row['geometry'].exterior.coords]
    color = 'green' if is_sufficient else 'red'
    folium.Polygon(coords, color=color, fill=True, fill_opacity=0.4, 
                   popup=f"Field {row['field_id']}: {row['crop_type']} (Demand: {row['total_field_demand']:,} m3)").add_to(m)

# Добавление текстового вывода на карту
folium.Popup(f"Анализ водного баланса: {status}. Дефицит/Профицит: {balance:,} м3").add_to(m)

# Сохранение карты
m.save("120.html")