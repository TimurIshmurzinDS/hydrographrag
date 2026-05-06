import folium
from geopy.distance import geodesic

def solve_river_distance():
    # 1. Координаты точек впадения (устьев) рек
    # Примечание: Координаты являются приблизительными значениями точек слияния с р. Или
    # Точка впадения реки Каратал в р. Или
    karatal_mouth = (43.4850, 78.6520) 
    # Точка впадения реки Улькен Алматы (Большая Алматы) в систему р. Или
    ulken_almaty_mouth = (43.2510, 77.1540)

    # 2. Расчет расстояния с использованием геодезического метода (WGS-84)
    distance = geodesic(karatal_mouth, ulken_almaty_mouth).kilometers

    print(f"Расстояние между точками впадения рек Каратал и Улькен Алматы: {distance:.2f} км")

    # 3. Визуализация на карте
    # Центрируем карту между двумя точками
    map_center = [
        (karatal_mouth[0] + ulken_almaty_mouth[0]) / 2,
        (karatal_mouth[1] + ulken_almaty_mouth[1]) / 2
    ]
    
    m = folium.Map(location=map_center, zoom_start=7, control_scale=True)

    # Добавление маркера для р. Каратал
    folium.Marker(
        location=karatal_mouth,
        popup=f"Устье р. Каратал",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    # Добавление маркера для р. Улькен Алматы
    folium.Marker(
        location=ulken_almaty_mouth,
        popup=f"Устье р. Улькен Алматы",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # Рисуем линию между точками
    line_coords = [karatal_mouth, ulken_almaty_mouth]
    folium.PolyLine(
        locations=line_coords,
        color='green',
        weight=3,
        opacity=0.8,
        tooltip=f"Расстояние: {distance:.2f} км"
    ).add_to(m)

    # 4. Сохранение карты
    m.save("102.html")
    print("Карта успешно сохранена в файл 102.html")

if __name__ == "__main__":
    solve_river_distance()