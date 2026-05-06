import requests
import folium

def get_overpass_data(query):
    url = "http://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': query})
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    # 1. Overpass QL запрос: 
    # Находим реку Уржар, затем находим все пути (ways), которые пересекаются с ней
    # и имеют тег waterway.
    query = """
    [out:json][timeout:25];
    way["name"="Уржар"]["waterway"]->.main_river;
    node(w.main_river)->.nodes;
    way(bn.nodes)["waterway"]->.all_connected;
    .main_river out geom;
    .all_connected out geom;
    """
    
    data = get_overpass_data(query)
    if not data:
        print("Ошибка при получении данных из Overpass API")
        return

    elements = data.get('elements', [])
    
    main_river_segments = []
    tributaries = []
    
    # Разделяем основной русло и притоки
    for elem in elements:
        if elem['type'] == 'way':
            if elem.get('tags', {}).get('name') == 'Уржар':
                main_river_segments.append(elem)
            else:
                tributaries.append(elem)

    # Создаем карту, центрированную по первой точке основной реки
    if not main_river_segments:
        print("Река Уржар не найдена.")
        return

    first_coord = main_river_segments[0]['geometry'][0]
    m = folium.Map(location=[first_coord['lat'], first_coord['lon']], zoom_start=8)

    # Отрисовка основного русла
    for segment in main_river_segments:
        coords = [[p['lat'], p['lon']] for p in segment['geometry']]
        folium.PolyLine(coords, color='blue', weight=4, opacity=0.8, tooltip="Река Уржар").add_to(m)

    # Отрисовка притоков и поиск точек слияния
    found_tributaries_coords = []
    
    for trib in tributaries:
        name = trib.get('tags', {}).get('name', 'Безымянный приток')
        coords = [[p['lat'], p['lon']] for p in trib['geometry']]
        
        # Рисуем линию притока
        folium.PolyLine(coords, color='lightblue', weight=2, opacity=0.6, tooltip=name).add_to(m)
        
        # Точка слияния (обычно это один из концов притока, который совпадает с точкой основной реки)
        # Для упрощения возьмем первую точку притока как репрезентативную для координат
        confluence_point = coords[0]
        found_tributaries_coords.append({'name': name, 'coords': confluence_point})
        
        # Добавляем маркер в точку слияния
        folium.CircleMarker(
            location=confluence_point,
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"Приток: {name}"
        ).add_to(m)

    # Вывод координат притоков в консоль
    print("Найденные притоки и их координаты (точки слияния/начала):")
    for trib in found_tributaries_coords:
        print(f"{trib['name']}: {trib['coords']}")

    # Сохранение карты
    m.save("91.html")
    print("\nКарта успешно сохранена в файл 91.html")

if __name__ == "__main__":
    main()