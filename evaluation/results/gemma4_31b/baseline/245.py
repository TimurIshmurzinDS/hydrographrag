import folium
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Вычисляет расстояние между двумя точками на сфере (в километрах).
    """
    # Радиус Земли в километрах
    R = 6371.0 
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return R * c

def calculate_black_hole_mass(river_length):
    """
    Вычисляет массу черной дыры на основе длины реки.
    Используется гипотетическая модель масштабирования.
    """
    # Масса Солнца в кг
    SOLAR_MASS = 1.989e30 
    # Гипотетическая константа Караоя (в единицах 1/км)
    # Допустим, 1 км реки соответствует 10^12 масс Солнца в нашей модели
    KARAOY_CONSTANT = 1e12 
    
    mass = river_length * KARAOY_CONSTANT * SOLAR_MASS
    return mass

# 1. Координаты реки Караой (упрощенная аппроксимация русла)
# В реальном GIS-проекте здесь был бы загружен GeoJSON или Shapefile
karaoy_coords = [
    (49.512, 85.210), 
    (49.530, 85.250), 
    (49.550, 85.300), 
    (49.580, 85.380), 
    (49.610, 85.450)
]

# 2. Вычисление общей длины реки
total_length = 0.0
for i in range(len(karaoy_coords) - 1):
    p1 = karaoy_coords[i]
    p2 = karaoy_coords[i+1]
    total_length += haversine(p1[1], p1[0], p2[1], p2[0])

# 3. Вычисление массы черной дыры
bh_mass = calculate_black_hole_mass(total_length)

print(f"Вычисленная длина реки Караой: {total_length:.2f} км")
print(f"Расчетная масса черной дыры: {bh_mass:.2e} кг")

# 4. Визуализация на карте
# Центрируем карту на среднем значении координат
m = folium.Map(location=[49.56, 85.33], zoom_start=10)

# Рисуем линию реки
folium.PolyLine(
    locations=karaoy_coords, 
    color='blue', 
    weight=5, 
    opacity=0.8, 
    tooltip="Река Караой"
).add_to(m)

# Добавляем маркеры начала и конца
folium.Marker(location=karaoy_coords[0], popup="Исток (условно)").add_to(m)
folium.Marker(location=karaoy_coords[-1], popup="Устье (условно)").add_to(m)

# Сохранение карты
m.save("245.html")
print("Карта сохранена в файл 245.html")