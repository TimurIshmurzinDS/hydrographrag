import math
from folium import Map, Marker

# Координаты места измерения ширины реки Караой (примерные координаты)
lat_karaoy = 51.283611
lon_karaoy = 76.940278

# Координаты Альфы Центавра в галактической системе отсчета (переведем их в географические координаты Земли)
# Для примера возьмем приближенные географические координаты Альфы Центавра
lat_alpha_centauri = -60.832711
lon_alpha_centauri = 219.902345

# Функция для расчета расстояния между двумя точками на сфере Земли (формула Гаверсинса)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Радиус Земли в км
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Расчет расстояния до Альфы Центавра
distance_to_alpha_centauri = haversine(lat_karaoy, lon_karaoy, lat_alpha_centauri, lon_alpha_centauri)
print(f"Расстояние до Альфы Центавра: {distance_to_alpha_centauri} км")

# Визуализация на карте
m = Map(location=[lat_karaoy, lon_karaoy], zoom_start=10)

# Добавление маркеров для места измерения ширины реки Караой и Альфы Центавра
Marker([lat_karaoy, lon_karaoy], popup='Место измерения ширины реки Караой').add_to(m)
Marker([lat_alpha_centauri, lon_alpha_centauri], popup='Альфа Центавр').add_to(m)

# Сохранение карты
m.save("253.html")