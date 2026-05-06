import folium
import random
import math

def calculate_distance(coord1, coord2):
    """Вычисляет упрощенное расстояние между двумя точками (в градусах)"""
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def space_game_koktal():
    # 1. Координаты области реки Коктал (приблизительный центр и границы)
    # Центр региона
    center_lat, center_lon = 43.65, 80.20 
    # Границы для генерации объектов (bounding box)
    lat_min, lat_max = 43.55, 43.75
    lon_min, lon_max = 80.10, 80.30

    # 2. Инициализация игровых объектов
    player_base = [43.65, 80.20]
    resources = []
    hazards = []
    
    # Генерируем 10 кристаллов энергии
    for _ in range(10):
        resources.append([random.uniform(lat_min, lat_max), random.uniform(lon_min, lon_max)])
        
    # Генерируем 3 зоны космических аномалий
    for _ in range(3):
        hazards.append([random.uniform(lat_min, lat_max), random.uniform(lon_min, lon_max)])

    # 3. Создание карты (используем темный стиль для эффекта космоса/ночного сканирования)
    # Примечание: folium не имеет встроенного 'dark' стиля без внешних тайлов, 
    # поэтому используем стандартный, но добавим стилизованные маркеры.
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB dark_matter')

    # Добавляем Командный Центр
    folium.Marker(
        location=player_base,
        popup="Командный Центр 'Коктал-1'",
        icon=folium.Icon(color='blue', icon='home')
    ).add_to(m)

    # 4. Логика "захвата" и визуализация ресурсов
    captured_resources = []
    capture_radius = 0.05  # Радиус действия базы

    for i, res in enumerate(resources):
        dist = calculate_distance(player_base, res)
        
        if dist <= capture_radius:
            # Ресурс захвачен
            captured_resources.append(res)
            color = 'green'
            status = "Захвачен"
        else:
            color = 'yellow'
            status = "Доступен для разведки"

        # Добавляем ресурс на карту
        folium.CircleMarker(
            location=res,
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"Кристалл #{i+1}: {status}"
        ).add_to(m)

        # Если ресурс захвачен, рисуем линию связи с базой
        if dist <= capture_radius:
            folium.PolyLine(
                locations=[player_base, res],
                color='cyan',
                weight=2,
                opacity=0.6,
                dash_array='5, 10'
            ).add_to(m)

    # 5. Визуализация аномалий
    for haz in hazards:
        folium.Circle(
            location=haz,
            radius=1000, # 1 км
            color='red',
            fill=True,
            fill_opacity=0.4,
            popup="ОПАСНОСТЬ: Космическая аномалия!"
        ).add_to(m)

    # Сохранение карты
    m.save("239.html")
    print("Game map generated successfully as 239.html")

if __name__ == "__main__":
    space_game_koktal()