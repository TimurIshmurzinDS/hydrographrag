import folium
from geopy.distance import geodesic

def solve_refreshing_drink_gis():
    # 1. Координаты объектов (Приблизительные координаты для реки Баскан, Калмыкия)
    # Точка забора льда на реке Баскан
    ice_source_coords = [46.2500, 44.1000] 
    # Точка приготовления (например, ближайший лагерь или поселок)
    prep_station_coords = [46.3000, 44.2000]

    # 2. Расчет расстояния для оценки времени транспортировки (чтобы лед не растаял)
    distance = geodesic(ice_source_coords, prep_station_coords).kilometers
    
    # 3. Определение "рецепта" в контексте моделирования
    recipe = (
        "Рецепт освежающего напитка 'Басканский лед':\n"
        f"1. Забрать лед в точке {ice_source_coords}.\n"
        f"2. Транспортировать его на расстояние {distance:.2f} км до станции приготовления.\n"
        "3. Добавить в стакан свежевыжатый сок или мяту.\n"
        "4. Подавать охлажденным, используя природный лед реки Баскан."
    )
    
    print("--- Модель логистики напитка ---")
    print(recipe)

    # 4. Визуализация на карте
    # Создаем карту, центрированную между двумя точками
    m = folium.Map(location=[(ice_source_coords[0] + prep_station_coords[0])/2, 
                             (ice_source_coords[1] + prep_station_coords[1])/2], 
                   zoom_start=12, 
                   tiles='OpenStreetMap')

    # Маркер точки забора льда
    folium.Marker(
        location=ice_source_coords,
        popup="Источник льда: Река Баскан",
        icon=folium.Icon(color='blue', icon='snowflake', prefix='fa')
    ).add_to(m)

    # Маркер точки приготовления
    folium.Marker(
        location=prep_station_coords,
        popup="Станция приготовления напитка",
        icon=folium.Icon(color='green', icon='glass', prefix='fa')
    ).add_to(m)

    # Линия маршрута транспортировки
    folium.PolyLine(
        locations=[ice_source_coords, prep_station_coords],
        color='blue',
        weight=5,
        opacity=0.7,
        tooltip=f"Маршрут доставки льда ({distance:.2f} км)"
    ).add_to(m)

    # Сохранение карты
    m.save("267.html")
    print("\nКарта маршрута сохранена в файл 267.html")

if __name__ == "__main__":
    # Установка необходимых библиотек: pip install folium geopy
    solve_refreshing_drink_gis()