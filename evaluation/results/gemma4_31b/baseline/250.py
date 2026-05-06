import numpy as np
import folium
import math

def calculate_satellite_track(duration_min=90, step_sec=60):
    """
    Рассчитывает упрощенную траекторию спутника (Ground Track) 
    над заданной областью.
    """
    # Константы
    R_EARTH = 6371.0  # Радиус Земли в км
    MU = 398600.4418  # Гравитационный параметр Земли (км^3/с^2)
    
    # Параметры орбиты
    altitude = 550.0   # Высота LEO в км
    inclination = np.radians(45)  # Наклонение орбиты
    r = R_EARTH + altitude
    
    # Орбитальный период T = 2 * pi * sqrt(r^3 / MU)
    period = 2 * np.pi * np.sqrt(r**3 / MU)
    omega_sat = 2 * np.pi / period  # Угловая скорость спутника
    omega_earth = 7.2921159e-5      # Угловая скорость вращения Земли (рад/с)
    
    track = []
    
    # Моделируем пролет над регионом реки Тентек (примерно 48°N, 66°E)
    # Смещаем начальную фазу, чтобы спутник пролетал над целью
    for t in range(0, duration_min * 60, step_sec):
        # Положение в орбитальной плоскости
        theta = omega_sat * t
        
        # Координаты в ECEF (упрощенно)
        # x = r * cos(theta)
        # y = r * sin(theta) * cos(inclination)
        # z = r * sin(theta) * sin(inclination)
        
        # Пересчет в широту и долготу
        lat = np.degrees(np.arcsin(np.sin(theta) * np.sin(inclination)))
        
        # Долгота учитывает вращение Земли
        lon_relative = np.degrees(np.arctan2(np.sin(theta) * np.cos(inclination), np.cos(theta)))
        lon_earth = lon_relative - np.degrees(omega_earth * t)
        
        # Центрируем долготу вокруг реки Тентек (~66.0)
        lon = (lon_earth + 66.0) % 360
        if lon > 180: lon -= 360
        
        track.append([lat, lon])
        
    return track

def get_tentek_river_network():
    """
    Возвращает синтетические координаты сети притоков реки Тентек.
    (В реальном проекте здесь будет загрузка GeoJSON/Shapefile)
    """
    # Основное русло реки Тентек (упрощенно)
    main_stem = [
        [48.5, 65.2], [48.6, 65.5], [48.7, 65.8], [48.8, 66.1], [48.9, 66.4]
    ]
    # Притоки
    tributaries = [
        [[48.4, 65.3], [48.5, 65.4]], # Приток 1
        [[48.6, 65.6], [48.7, 65.6]], # Приток 2
        [[48.7, 65.9], [48.8, 65.9]], # Приток 3
        [[48.8, 66.2], [48.7, 66.3]], # Приток 4
    ]
    return main_stem, tributaries

def main():
    # 1. Получаем данные о реке
    main_stem, tributaries = get_tentek_river_network()
    
    # 2. Рассчитываем орбиту спутника
    satellite_path = calculate_satellite_track()
    
    # 3. Создаем карту, центрированную на регионе
    m = folium.Map(location=[48.7, 65.8], zoom_start=7, tiles='CartoDB positron')
    
    # 4. Визуализируем речную сеть
    # Основное русло - синий цвет
    folium.PolyLine(main_stem, color='blue', weight=4, opacity=0.8, tooltip="Река Тентек (основное русло)").add_to(m)
    
    # Притоки - голубой цвет
    for i, trib in enumerate(tributaries):
        folium.PolyLine(trib, color='skyblue', weight=2, opacity=0.6, tooltip=f"Приток {i+1}").add_to(m)
        
    # 5. Визуализируем орбиту спутника
    folium.PolyLine(satellite_path, color='red', weight=2, opacity=0.7, 
                    dash_array='5, 10', tooltip="Траектория спутника (Ground Track)").add_to(m)
    
    # Добавляем маркер текущего положения спутника (последняя точка)
    folium.Marker(
        location=satellite_path[-1],
        popup="Текущая позиция спутника",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # Сохранение результата
    m.save("250.html")
    print("Моделирование завершено. Карта сохранена в файл 250.html")

if __name__ == "__main__":
    main()