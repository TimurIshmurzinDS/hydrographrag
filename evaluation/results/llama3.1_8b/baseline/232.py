import folium
from math import sin, cos, sqrt, atan2, radians

# Функция для преобразования уровня воды в географические координаты
def water_level_to_coordinates(water_level):
    # Примерные значения для реки Каскелен (Казахстан)
    latitude = 43.0333
    longitude = 76.1667
    
    return radians(latitude), radians(longitude)

# Функция для расчета расстояния между двумя объектами в пространстве
def calculate_distance(lat1, lon1, lat2, lon2):
    # Формула расстояния между двумя точками на сфере (Земле)
    R = 6371.0
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c

# Функция для определения траектории полета на Луну
def calculate_trajectory(water_level):
    # Примерные значения для скорости и направления движения
    speed = 10000.0  # км/ч
    direction = radians(45)  # градусы
    
    lat, lon = water_level_to_coordinates(water_level)
    
    distance_to_moon = calculate_distance(lat, lon, radians(28.5), radians(-13.2))  # Координаты Луны
    
    trajectory = []
    
    for i in range(int(distance_to_moon / speed)):
        new_lat = lat + (speed * cos(direction) / 1000)
        new_lon = lon + (speed * sin(direction) / 1000)
        
        trajectory.append((new_lat, new_lon))
        
        lat, lon = new_lat, new_lon
    
    return trajectory

# Визуализация траектории на карте
def visualize_trajectory(trajectory):
    m = folium.Map(location=[43.0333, 76.1667], zoom_start=10)
    
    for i in range(len(trajectory) - 1):
        folium.PolyLine([trajectory[i], trajectory[i + 1]], color='blue').add_to(m)
    
    m.save("232.html")

# Основная функция
def main():
    water_level = 100.0  # Примерное значение уровня воды в реке Каскелен
    
    trajectory = calculate_trajectory(water_level)
    
    visualize_trajectory(trajectory)

if __name__ == "__main__":
    main()