import folium
from shapely.geometry import Polygon

# Определение координат участков рек Sarykan River и Temirlik River
sarykan_river_coords = [
    (43.123, 76.543),
    (43.124, 76.544),
    (43.125, 76.545),
    # Добавьте больше точек для полного описания реки
]

temirlik_river_coords = [
    (43.126, 76.546),
    (43.127, 76.547),
    (43.128, 76.548),
    # Добавьте больше точек для полного описания реки
]

# Создание геометрий для участков рек
sarykan_river_polygon = Polygon(sarykan_river_coords)
temirlik_river_polygon = Polygon(temirlik_river_coords)

# Определение площадей участков (в квадратных метрах)
sarykan_river_area = sarykan_river_polygon.area
temirlik_river_area = temirlik_river_polygon.area

# Оценка средней глубины воды в реках (в метрах)
average_depth_sarykan = 10  # Примерное значение, замените на реальное
average_depth_temirlik = 5   # Примерное значение, замените на реальное

# Расчет объема воды для каждой реки
volume_sarykan = sarykan_river_area * average_depth_sarykan
volume_temirlik = temirlik_river_area * average_depth_temirlik

# Общий объем воды
total_volume = volume_sarykan + volume_temirlik

print(f"Общий объем воды, доступный для полива: {total_volume} кубических метров")

# Визуализация на карте с использованием folium
m = folium.Map(location=[43.125, 76.545], zoom_start=10)

folium.Polygon(sarykan_river_coords, color='blue', fill=True, fill_color='blue').add_to(m)
folium.Polygon(temirlik_river_coords, color='green', fill=True, fill_color='green').add_to(m)

m.save("118.html")