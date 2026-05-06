import folium
import geopandas as gpd
from shapely.geometry import LineString, Polygon, Point
import random

def generate_karaoy_basin_data():
    """
    Генерация синтетических данных для бассейна реки Караой.
    Координаты приблизительно соответствуют региону Центральной Азии.
    """
    # 1. Создаем линию реки Караой (упрощенно)
    river_coords = [
        (48.5, 65.0), (48.6, 65.2), (48.7, 65.3), 
        (48.8, 65.5), (48.9, 65.7), (49.0, 65.8)
    ]
    river_line = LineString(river_coords)

    # 2. Создаем случайные поля вокруг реки
    fields = []
    for i in range(15):
        # Генерируем случайную точку вблизи реки
        base_lat = random.uniform(48.4, 49.1)
        base_lon = random.uniform(64.9, 66.0)
        
        # Создаем небольшой квадратный полигон вокруг точки
        offset = 0.01
        field_poly = Polygon([
            (base_lat, base_lon),
            (base_lat + offset, base_lon),
            (base_lat + offset, base_lon + offset),
            (base_lat, base_lon + offset),
            (base_lat, base_lon)
        ])
        fields.append(field_poly)
    
    return river_line, fields

def calculate_irrigation_status(river, fields, threshold=0.05):
    """
    Определяет статус полива на основе расстояния до реки.
    threshold: порог расстояния в градусах (упрощенно)
    """
    results = []
    for field in fields:
        centroid = field.centroid
        distance = centroid.distance(river)
        
        status = "Irrigated" if distance <= threshold else "Needs Infrastructure"
        results.append({
            "geometry": field,
            "distance": distance,
            "status": status
        })
    return results

def main():
    # Генерация данных
    river, fields = generate_karaoy_basin_data()
    
    # Анализ полива
    irrigation_data = calculate_irrigation_status(river, fields)
    
    # Создание карты Folium
    # Центрируем карту на среднем значении координат
    m = folium.Map(location=[48.7, 65.4], zoom_start=8, tiles='OpenStreetMap')
    
    # Добавление реки на карту
    river_coords_folium = [(p[0], p[1]) for p in river.coords]
    folium.PolyLine(river_coords_folium, color="blue", weight=5, opacity=0.8, tooltip="Река Караой").add_to(m)
    
    # Добавление полей на карту
    for item in irrigation_data:
        poly_coords = [
            (p[0], p[1]) for p in item["geometry"].exterior.coords
        ]
        
        # Цвет: Зеленый если полив есть, Красный если нет
        color = "green" if item["status"] == "Irrigated" else "red"
        
        folium.Polygon(
            locations=poly_coords,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.4,
            popup=f"Статус: {item['status']}<br>Дистанция: {item['distance']:.4f}"
        ).add_to(m)

    # Сохранение карты
    m.save("266.html")
    print("Моделирование завершено. Карта сохранена в файл 266.html")

if __name__ == "__main__":
    main()