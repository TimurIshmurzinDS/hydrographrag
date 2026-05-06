import folium
from geopy.distance import geodesic

def main():
    # 1. Координаты точек (приблизительные географические координаты)
    # Устье реки Дос (впадение в Урал)
    dos_mouth = (51.152, 58.615) 
    # Начало (исток) реки Емель
    emel_source = (51.620, 61.850)

    # 2. Вычисление расстояния с использованием эллипсоида WGS-84
    distance = geodesic(dos_mouth, emel_source).kilometers

    print(f"Расстояние между устьем реки Дос и началом реки Емель составляет: {distance:.2f} км")

    # 3. Визуализация на карте
    # Центрируем карту между двумя точками
    map_center = [
        (dos_mouth[0] + emel_source[0]) / 2,
        (dos_mouth[1] + emel_source[1]) / 2
    ]
    
    m = folium.Map(location=map_center, zoom_start=6, control_scale=True)

    # Добавление маркера для устья р. Дос
    folium.Marker(
        location=dos_mouth,
        popup=f"Устье реки Дос\nКоординаты: {dos_mouth}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    # Добавление маркера для истока р. Емель
    folium.Marker(
        location=emel_source,
        popup=f"Начало реки Емель\nКоординаты: {emel_source}",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(m)

    # Рисование линии между точками
    folium.PolyLine(
        locations=[dos_mouth, emel_source],
        color='red',
        weight=3,
        opacity=0.8,
        tooltip=f"Расстояние: {distance:.2f} км"
    ).add_to(m)

    # 4. Сохранение карты
    m.save("92.html")
    print("Карта успешно сохранена в файл 92.html")

if __name__ == "__main__":
    main()