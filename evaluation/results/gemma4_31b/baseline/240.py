import folium
import numpy as np
from shapely.geometry import LineString, Point, Polygon

def generate_kaskelen_model():
    # 1. Координаты реки Каскелен (упрощенная аппроксимация русла в районе Алматинской области)
    # Река течет примерно с юго-востока на северо-запад
    river_coords = [
        [43.15, 77.20], [43.12, 77.15], [43.10, 77.10], 
        [43.08, 77.05], [43.05, 77.00], [43.02, 76.95]
    ]
    river_line = LineString(river_coords)

    # 2. Моделирование сезонных колебаний (Буферные зоны)
    # Низкий уровень (русло) - 100м, Высокий уровень (паводок) - 1500м
    # В folium мы используем упрощенные круги/полигоны для визуализации зон
    
    # Создаем карту, центрированную на реке
    m = folium.Map(location=[43.08, 77.08], zoom_start=11, tiles='OpenStreetMap')

    # Отрисовка русла реки
    folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Река Каскелен").add_to(m)

    # 3. Моделирование "Зон плодородия" (Сезонные поймы)
    # Генерируем точки вдоль реки для создания эффекта поймы
    flood_zone_coords = []
    for coord in river_coords:
        # Создаем небольшое смещение для имитации ширины поймы
        flood_zone_coords.append([coord[0] + 0.01, coord[1] + 0.01])
        flood_zone_coords.append([coord[0] - 0.01, coord[1] - 0.01])
    
    # Визуализируем зону выращивания пшеницы (зеленый цвет)
    # Для простоты используем Circle в ключевых точках
    for coord in river_coords:
        folium.Circle(
            location=coord,
            radius=1500, 
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.2,
            tooltip="Зона сезонного затопления (Поля пшеницы)"
        ).add_to(m)

    # 4. Размещение инфраструктуры
    # Мельница: ставим в точку с предполагаемым перепадом высот (середина реки)
    mill_loc = [43.10, 77.10]
    folium.Marker(
        location=mill_loc,
        popup="Водяная мельница (Энергия реки)",
        icon=folium.Icon(color='blue', icon='cog', prefix='fa')
    ).add_to(m)

    # Пекарня: ставим в логистическом центре между полями и мельницей
    bakery_loc = [43.08, 77.12]
    folium.Marker(
        location=bakery_loc,
        popup="Пекарня (Финальный продукт)",
        icon=folium.Icon(color='red', icon='shopping-cart', prefix='fa')
    ).add_to(m)

    # 5. Визуализация логистической цепочки "От реки к хлебу"
    chain_coords = [
        [43.15, 77.20], # Поля
        mill_loc,       # Мельница
        bakery_loc      # Пекарня
    ]
    folium.PolyLine(chain_coords, color="orange", weight=3, dash_array='5, 10', tooltip="Цепочка производства хлеба").add_to(m)

    # Сохранение карты
    m.save("240.html")
    print("Modeling complete. Map saved as 240.html")

if __name__ == "__main__":
    generate_kaskelen_model()