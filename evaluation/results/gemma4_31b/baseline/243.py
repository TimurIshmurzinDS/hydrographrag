import numpy as np
import folium
from scipy.interpolate import CubicSpline

def model_river_kumbel():
    # 1. Опорные координаты реки Кумбель (симуляция точек русла)
    # В реальном сценарии здесь будут данные из Shape-файла или GeoJSON
    # Формат: [широта, долгота]
    control_points = np.array([
        [52.1200, 45.3100],
        [52.1350, 45.3500],
        [52.1500, 45.3800],
        [52.1400, 45.4200],
        [52.1600, 45.4500],
        [52.1800, 45.4800],
        [52.2000, 45.5200]
    ])

    lats = control_points[:, 0]
    lons = control_points[:, 1]

    # 2. Параметризация
    # Создаем параметр t (индекс точки), чтобы интерполировать координаты независимо
    t = np.arange(len(lats))
    
    # 3. Применение алгоритма Кубического Сплайна
    # bc_type='natural' обеспечивает естественное продолжение линии на концах
    cs_lat = CubicSpline(t, lats, bc_type='natural')
    cs_lon = CubicSpline(t, lons, bc_type='natural')

    # 4. Генерация плотного массива точек для плавности линии
    t_dense = np.linspace(0, len(lats) - 1, 200)
    smooth_lats = cs_lat(t_dense)
    smooth_lons = cs_lon(t_dense)
    
    river_coords = np.column_stack((smooth_lats, smooth_lons))

    # 5. Визуализация с помощью folium
    # Центрируем карту по средней точке
    center_lat = np.mean(lats)
    center_lon = np.mean(lons)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles='OpenStreetMap')

    # Рисуем интерполированную реку (синяя линия)
    folium.PolyLine(
        river_coords, 
        color='blue', 
        weight=4, 
        opacity=0.8, 
        tooltip='Модель русла реки Кумбель (Cubic Spline)'
    ).add_to(m)

    # Отмечаем опорные точки (красные маркеры)
    for point in control_points:
        folium.CircleMarker(
            location=[point[0], point[1]],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            popup='Опорная точка'
        ).add_to(m)

    # Сохранение результата
    m.save("243.html")
    print("Моделирование завершено. Карта сохранена в файл 243.html")

if __name__ == "__main__":
    model_river_kumbel()