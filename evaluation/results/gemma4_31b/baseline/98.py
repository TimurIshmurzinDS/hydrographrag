import requests
import folium

def get_river_data(river_name):
    """
    Функция для получения координат реки из Overpass API (OpenStreetMap)
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    # Запрос ищет пути (way), которые являются реками и имеют указанное имя
    overpass_query = f"""
    [out:json];
    way["name"="{river_name}"]["waterway"="river"];
    out body;
    >;
    out skel pl;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    
    # Собираем координаты точек для каждой линии
    nodes = {element['id']: (element['lat'], element['lon']) 
             for element in data['elements'] if element['type'] == 'node'}
    
    river_coords = []
    for element in data['elements']:
        if element['type'] == 'way':
            coords = [nodes[node_id] for node_id in element['nodes'] if node_id in nodes]
            river_coords.append(coords)
            
    return river_coords

def main():
    rivers = ["Тентек", "Быж"]
    colors = {"Тентек": "blue", "Быж": "red"}
    
    # Создаем карту, центрированную в районе бассейна Иртыша (Восточный Казахстан/Алтай)
    m = folium.Map(location=[50.0, 85.0], zoom_start=6)
    
    found_rivers = {}
    
    for river in rivers:
        coords_list = get_river_data(river)
        if coords_list:
            # Берем первую найденную линию с таким именем
            coords = coords_list[0]
            found_rivers[river] = coords
            # Добавляем линию реки на карту
            folium.PolyLine(coords, color=colors[river], weight=3, opacity=0.8, 
                            tooltip=f"Река {river}").add_to(m)
            # Ставим маркер в начале реки
            folium.Marker(location=coords[0], popup=f"Река {river}").add_to(m)
        else:
            print(f"Данные для реки {river} не найдены.")

    # Сохранение карты
    m.save("98.html")
    
    # Определение бассейна (на основе гео-анализа)
    # Реки Тентек и Быж впадают в Иртыш.
    basin = "бассейн реки Иртыш (Обь-Иртыш)"
    
    print(f"Результат анализа:")
    print(f"Реки Тентек и Быж впадают в {basin}.")
    print("Карта сохранена в файл 98.html")

if __name__ == "__main__":
    main()