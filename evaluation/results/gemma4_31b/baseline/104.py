import osmnx as ox
import geopandas as gpd
import folium
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points

def solve_river_task():
    # 1. Настройка параметров поиска
    # Реки находятся в Казахстане. Используем Overpass API через osmnx.
    river_shyzhyn_name = "Шыжын"
    river_dos_name = "Дос"
    
    print("Загрузка данных из OpenStreetMap...")
    try:
        # Запрос геометрий рек по именам
        # Мы ищем объекты с тегом waterway=river или waterway=stream
        query_shyzhyn = f'way["name"~"{river_shyzhyn_name}", i]["waterway"];'
        query_dos = f'way["name"~"{river_dos_name}", i]["waterway"];'
        
        # Получаем данные
        gdf_shyzhyn = ox.features_from_overpass(tags={"waterway": True}, 
                                               params={"name": river_shyzhyn_name})
        gdf_dos = ox.features_from_overpass(tags={"waterway": True}, 
                                             params={"name": river_dos_name})
        
        # Оставляем только линейные объекты
        shyzhyn_lines = gdf_shyzhyn[gdf_shyzhyn.geometry.type.isin(['LineString', 'MultiLineString'])]
        dos_lines = gdf_dos[gdf_dos.geometry.type.isin(['LineString', 'MultiLineString'])]

        if shyzhyn_lines.empty or dos_lines.empty:
            print("Одна из рек не найдена в базе OSM.")
            return

        # 2. Проверка на приток (пересечение)
        # Объединяем все сегменты в одну геометрию для каждой реки
        geom_shyzhyn = shyzhyn_lines.unary_union
        geom_dos = dos_lines.unary_union

        if geom_shyzhyn.intersects(geom_dos):
            print(f"Подтверждено: Река {river_shyzhyn_name} является притоком реки {river_dos_name}.")
            
            # Находим точку слияния
            intersection = geom_shyzhyn.intersection(geom_dos)
            if intersection.geom_type == 'Point':
                confluence_point = intersection
            elif intersection.geom_type == 'MultiPoint':
                confluence_point = intersection.geoms[0]
            else:
                confluence_point = intersection.centroid
        else:
            print(f"Река {river_shyzhyn_name} не пересекается с рекой {river_dos_name}.")
            return

        # 3. Расчет расстояния
        # Перепроецируем в UTM для расчета в метрах (Казахстан обычно UTM zone 42N)
        # EPSG:32642 - WGS 84 / UTM zone 42N
        shyzhyn_utm = gpd.GeoSeries([geom_shyzhyn], crs="EPSG:4326").to_crs(epsg=32642).iloc[0]
        
        # Расстояние от истока (начало линии) до точки слияния
        # В упрощенном виде считаем общую длину русла притока
        distance_meters = shyzhyn_utm.length
        distance_km = distance_meters / 1000
        print(f"Расстояние по руслу реки Шыжын до слияния: {distance_km:.2f} км")

        # 4. Визуализация
        # Центр карты
        center_lat = confluence_point.y
        center_lon = confluence_point.x
        m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles='CartoDB positron')

        # Добавляем реку Дос (синий цвет)
        for _, row in dos_lines.iterrows():
            if row.geometry.type == 'LineString':
                coords = [(p[1], p[0]) for p in row.geometry.coords]
                folium.PolyLine(coords, color='blue', weight=3, opacity=0.7, label='Река Дос').add_to(m)
            elif row.geometry.type == 'MultiLineString':
                for line in row.geometry.geoms:
                    coords = [(p[1], p[0]) for p in line.coords]
                    folium.PolyLine(coords, color='blue', weight=3, opacity=0.7).add_to(m)

        # Добавляем реку Шыжын (красный цвет)
        for _, row in shyzhyn_lines.iterrows():
            if row.geometry.type == 'LineString':
                coords = [(p[1], p[0]) for p in row.geometry.coords]
                folium.PolyLine(coords, color='red', weight=3, opacity=0.8, label='Река Шыжын').add_to(m)
            elif row.geometry.type == 'MultiLineString':
                for line in row.geometry.geoms:
                    coords = [(p[1], p[0]) for p in line.coords]
                    folium.PolyLine(coords, color='red', weight=3, opacity=0.8).add_to(m)

        # Отметка точки слияния
        folium.Marker(
            location=[center_lat, center_lon],
            popup=f"Точка слияния\nРасстояние: {distance_km:.2f} км",
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

        m.save("104.html")
        print("Карта сохранена в файл 104.html")

    except Exception as e:
        print(f"Произошла ошибка при выполнении: {e}")

if __name__ == "__main__":
    solve_river_task()