import folium
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

def solve_watershed_intersection():
    # 1. Имитация геоданных (Координаты региона рек Эмель и Тентек, Казахстан)
    # В реальном сценарии здесь будет загрузка shape-файлов: gpd.read_file("basins.shp")
    
    # Примерные координаты границ бассейна реки Эмель
    emel_coords = [
        (44.0, 78.0), (44.5, 79.0), (43.5, 80.0), 
        (42.5, 79.0), (42.0, 77.0), (43.0, 76.0), (44.0, 78.0)
    ]
    # Примерные координаты границ бассейна реки Тентек
    tentek_coords = [
        (43.5, 80.0), (44.0, 81.0), (43.0, 82.0), 
        (42.0, 81.0), (42.5, 79.0), (43.5, 80.0)
    ]

    # Создание полигонов бассейнов
    emel_poly = Polygon(emel_coords)
    tentek_poly = Polygon(tentek_coords)

    # 2. Извлечение границ (водоразделов) как LineString
    emel_boundary = emel_poly.boundary
    tentek_boundary = tentek_poly.boundary

    # 3. Поиск точек пересечения водоразделов
    # intersection() возвращает геометрию пересечения (точку, несколько точек или линию)
    intersection = emel_boundary.intersection(tentek_boundary)

    intersection_points = []
    if intersection.geom_type == 'Point':
        intersection_points.append((intersection.y, intersection.x))
    elif intersection.geom_type == 'MultiPoint':
        for p in intersection.geoms:
            intersection_points.append((p.y, p.x))
    elif intersection.geom_type == 'LineString':
        # Если водоразделы совпадают на отрезке, берем начальную и конечную точки
        coords = list(intersection.coords)
        intersection_points.append((coords[0][1], coords[0][0]))
        intersection_points.append((coords[-1][1], coords[-1][0]))
    elif intersection.geom_type == 'MultiLineString':
        for line in intersection.geoms:
            coords = list(line.coords)
            intersection_points.append((coords[0][1], coords[0][0]))
            intersection_points.append((coords[-1][1], coords[-1][0]))

    # 4. Визуализация с помощью folium
    # Центрируем карту на регионе
    m = folium.Map(location=[43.0, 79.0], zoom_start=6, tiles='OpenStreetMap')

    # Добавляем бассейн Эмель
    folium.Polygon(
        locations=[(p[1], p[0]) for p in emel_coords],
        color="blue", weight=2, fill=True, fill_opacity=0.3, 
        popup="Бассейн р. Эмель"
    ).add_to(m)

    # Добавляем бассейн Тентек
    folium.Polygon(
        locations=[(p[1], p[0]) for p in tentek_coords],
        color="green", weight=2, fill=True, fill_opacity=0.3, 
        popup="Бассейн р. Тентек"
    ).add_to(m)

    # Добавляем точки пересечения водоразделов
    for idx, pt in enumerate(intersection_points):
        folium.Marker(
            location=pt,
            popup=f"Точка пересечения {idx+1}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    # Сохранение карты
    m.save("174.html")
    print(f"Analysis complete. Found {len(intersection_points)} key intersection points. Map saved as 174.html")

if __name__ == "__main__":
    solve_watershed_intersection()