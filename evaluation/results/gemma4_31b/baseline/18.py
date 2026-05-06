import folium
import geopandas as gpd
from shapely.geometry import LineString, Polygon

# 1. Имитация данных: Координаты реки Bayankol (условно в регионе Центральной Азии)
# В реальном проекте здесь будет загрузка из Shapefile или GeoJSON
river_coords = [
    (45.123, 68.456), 
    (45.150, 68.500), 
    (45.200, 68.550), 
    (45.250, 68.600)
]
river_geom = LineString(river_coords)
river_gdf = gpd.GeoDataFrame([{'river': 'Bayankol River', 'geometry': river_geom}], crs="EPSG:4326")

# 2. Имитация данных о зонах предупреждений о паводках (Полигоны)
# Создаем две зоны: одна пересекает реку, другая находится в стороне
warning_zones_coords = [
    # Зона 1: Пересекает реку (Опасная зона)
    Polygon([(45.140, 68.480), (45.160, 68.480), (45.160, 68.520), (45.140, 68.520)]),
    # Зона 2: В стороне (Безопасная зона)
    Polygon([(45.300, 68.700), (45.320, 68.700), (45.320, 68.720), (45.300, 68.720)])
]
warnings_gdf = gpd.GeoDataFrame([{'zone_id': i, 'level': 'High' if i==0 else 'Low', 'geometry': geom} 
                                 for i, geom in enumerate(warning_zones_coords)], crs="EPSG:4326")

# 3. Пространственный анализ: Проверка наличия предупреждений
# Проверяем, пересекается ли река с какой-либо из зон предупреждения
intersecting_zones = warnings_gdf[warnings_gdf.intersects(river_geom)]
has_warning = not intersecting_zones.empty

# Вывод результата в консоль
if has_warning:
    print(f"ВНИМАНИЕ: Для реки Bayankol River обнаружены активные предупреждения о сезонных паводках!")
    print(f"Количество затронутых зон: {len(intersecting_zones)}")
else:
    print("Предупреждений о сезонных паводках для реки Bayankol River не обнаружено.")

# 4. Визуализация на карте
# Центрирование карты по средней точке реки
center_lat = sum([p[0] for p in river_coords]) / len(river_coords)
center_lon = sum([p[1] for p in river_coords]) / len(river_coords)
m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles='CartoDB positron')

# Добавление реки на карту
folium.PolyLine(river_coords, color="blue", weight=4, opacity=0.8, tooltip="Bayankol River").add_to(m)

# Добавление зон предупреждения на карту
for idx, row in warnings_gdf.iterrows():
    # Получаем координаты полигона для folium
    coords = list(row['geometry'].exterior.coords)
    color = 'red' if row['geometry'].intersects(river_geom) else 'orange'
    status = 'Active Warning' if row['geometry'].intersects(river_geom) else 'Monitoring'
    
    folium.Polygon(
        locations=coords,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.4,
        tooltip=f"Zone {row['zone_id']}: {status}"
    ).add_to(m)

# Сохранение карты
m.save("18.html")
print("Карта сохранена в файл 18.html")