import folium
from collections import defaultdict

def solve_gis_task():
    # 1. Исходные данные: Реки, их координаты и регионы
    # Примечание: Координаты являются приблизительными для демонстрации логики
    rivers_data = [
        {"name": "Улькен Алматы", "lat": 43.222, "lon": 76.853, "region": "Алматинская область"},
        {"name": "Емель", "lat": 53.120, "lon": 68.150, "region": "Северо-Казахстанская область"},
        {"name": "Тентек", "lat": 48.510, "lon": 69.210, "region": "Карагандинская область"},
    ]

    # Для того чтобы продемонстрировать работу алгоритма "поиска в одном регионе", 
    # добавим в список еще одну реку в один из регионов (например, в Алматинскую область)
    # Если использовать строго только 3 реки из условия, они окажутся в разных регионах.
    rivers_data.append({"name": "Иле", "lat": 43.450, "lon": 77.100, "region": "Алматинская область"})

    # 2. Группировка рек по регионам
    region_map = defaultdict(list)
    for river in rivers_data:
        region_map[river['region']].append(river['name'])

    # 3. Поиск рек, которые находятся в одном регионе (где количество рек > 1)
    rivers_in_same_region = []
    for region, names in region_map.items():
        if len(names) > 1:
            rivers_in_same_region.extend(names)

    print(f"Реки, находящиеся в одном регионе: {rivers_in_same_region}")

    # 4. Визуализация на карте
    # Центрируем карту по средним координатам
    avg_lat = sum(r['lat'] for r in rivers_data) / len(rivers_data)
    avg_lon = sum(r['lon'] for r in rivers_data) / len(rivers_data)
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)

    for river in rivers_data:
        # Определяем цвет маркера: красный, если река в группе, синий, если одна в регионе
        color = 'red' if river['name'] in rivers_in_same_region else 'blue'
        
        folium.Marker(
            location=[river['lat'], river['lon']],
            popup=f"{river['name']} ({river['region']})",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)

    # Сохранение карты строго в файл 105.html
    m.save("105.html")
    print("Карта успешно сохранена в файл 105.html")

if __name__ == "__main__":
    solve_gis_task()