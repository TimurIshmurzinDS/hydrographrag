import folium
from geopy.distance import geodesic

def solve_mars_potato_problem():
    # 1. Координаты ключевых точек (Земля)
    # Река Талгар (примерная точка в предгорьях Заилийского Алатау)
    talgar_river = [43.15, 77.55] 
    # Космодром Байконур (точка отправки на Марс)
    baikonur = [45.96, 63.32]
    
    # 2. Расчеты логистики на Земле
    dist_earth = geodesic(talgar_river, baikonur).kilometers
    
    # 3. Константы для моделирования Марса
    avg_dist_earth_mars = 225_000_000  # км
    water_per_kg_potato = 1.0          # литры на 1 кг картофеля
    target_harvest_kg = 1000           # цель: 1 тонна картофеля
    
    total_water_needed = target_harvest_kg * water_per_kg_potato
    
    print(f"--- Анализ логистики ---")
    print(f"Расстояние от р. Талгар до Байконура: {dist_earth:.2f} км")
    print(f"Среднее расстояние до Марса: {avg_dist_earth_mars:,} км")
    print(f"Необходимый объем воды из р. Талгар для 1 тонны картофеля: {total_water_needed} литров")
    
    # 4. Визуализация земного сегмента (ГИС)
    # Создаем карту, центрированную между Талгаром и Байконуром
    m = folium.Map(location=[44.5, 70.0], zoom_start=5, tiles="CartoDB positron")
    
    # Маркер реки Талгар
    folium.Marker(
        location=talgar_river,
        popup=f"Источник: Река Талгар\nЗабор воды для Марса",
        icon=folium.Icon(color="blue", icon="tint")
    ).add_to(m)
    
    # Маркер Байконура
    folium.Marker(
        location=baikonur,
        popup="Космодром Байконур\nТочка отправки на Марс",
        icon=folium.Icon(color="red", icon="rocket")
    ).add_to(m)
    
    # Линия транспортировки воды по Земле
    folium.PolyLine(
        locations=[talgar_river, baikonur],
        color="blue",
        weight=3,
        opacity=0.7,
        tooltip="Маршрут доставки воды"
    ).add_to(m)
    
    # Добавляем текстовую аннотацию о Марсе
    folium.Popup(f"Цель: Доставить {total_water_needed}л воды на Марс").add_to(m)

    # Сохранение карты
    m.save("263.html")
    print("\nКарта земного сегмента логистики сохранена в файл '263.html'")

if __name__ == "__main__":
    solve_mars_potato_problem()