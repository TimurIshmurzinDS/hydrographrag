import folium
from geopy.distance import geodesic
import random

class RiverRobot:
    """Класс для управления симуляцией робота на реке Караой"""
    def __init__(self, start_coords):
        self.current_position = start_coords
        self.path_history = [start_coords]
        self.collected_data = []
        self.total_distance = 0.0

    def move_to(self, target_coords):
        """Перемещение робота в заданную точку с расчетом дистанции"""
        dist = geodesic(self.current_position, target_coords).meters
        self.total_distance += dist
        self.current_position = target_coords
        self.path_history.append(target_coords)
        print(f"Робот переместился в {target_coords}. Дистанция участка: {dist:.2f} м")

    def collect_sample(self, point_id):
        """Симуляция сбора данных в конкретной точке"""
        sample_value = round(random.uniform(6.5, 8.5), 2)  # Симуляция pH воды
        self.collected_data.append({"point": point_id, "ph": sample_value})
        print(f"Точка {point_id}: Сбор пробы завершен. pH = {sample_value}")

def main():
    # 1. Координаты русла реки Караой (упрощенная модель/аппроксимация)
    # В реальном проекте здесь будет загрузка GeoJSON файла
    karaoy_river_waypoints = [
        (42.1500, 78.5000), 
        (42.1550, 78.5100), 
        (42.1620, 78.5250), 
        (42.1700, 78.5400), 
        (42.1850, 78.5500), 
        (42.2000, 78.5650), 
        (42.2150, 78.5800)
    ]

    # 2. Инициализация робота в начальной точке
    robot = RiverRobot(start_coords=karaoy_river_waypoints[0])

    # 3. Цикл управления роботом
    print("Запуск системы управления роботом вдоль реки Караой...\n")
    for i in range(1, len(karaoy_river_waypoints)):
        target = karaoy_river_waypoints[i]
        
        # Команда: Переместиться
        robot.move_to(target)
        
        # Команда: Собрать данные
        robot.collect_sample(point_id=i)

    print(f"\nМиссия завершена. Общий путь: {robot.total_distance:.2f} метров.")

    # 4. Визуализация результатов на карте
    # Центрируем карту на среднем значении координат
    m = folium.Map(location=[42.18, 78.54], zoom_start=12, tiles='OpenStreetMap')

    # Рисуем русло реки (синяя линия)
    folium.PolyLine(karaoy_river_waypoints, color="blue", weight=4, opacity=0.8, tooltip="Русло реки Караой").add_to(m)

    # Добавляем маркеры точек сбора данных
    for idx, data in enumerate(robot.collected_data):
        coords = karaoy_river_waypoints[idx + 1]
        folium.CircleMarker(
            location=coords,
            radius=6,
            color="red",
            fill=True,
            fill_color="red",
            popup=f"Точка {idx+1}: pH {data['ph']}"
        ).add_to(m)

    # Маркер старта и финиша
    folium.Marker(karaoy_river_waypoints[0], popup="Старт робота", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(karaoy_river_waypoints[-1], popup="Финиш робота", icon=folium.Icon(color='black')).add_to(m)

    # Сохранение карты
    m.save("224.html")
    print("\nКарта маршрута сохранена в файл 224.html")

if __name__ == "__main__":
    main()