import requests
from datetime import datetime
from astropy.coordinates import get_body_barycentric_posvel, EarthLocation, SkyCoord
from astropy.time import Time
from astropy import units as u
import folium

# Шаг 1: Определение координат реки Талгар (примерные средние координаты)
talgar_coords = (42.8653, 79.0800)  # широта, долгота

# Шаг 2: Получение текущих эклиптических координат Юпитера
def get_jupiter_geocentric_coordinates():
    time_now = Time(datetime.utcnow())
    jupiter_posvel = get_body_barycentric_posvel('jupiter', time_now)
    jupiter_icrs = SkyCoord(jupiter_posvel[0], frame='icrs')
    return jupiter_icrs.ra.deg, jupiter_icrs.dec.deg

# Шаг 3: Расчет расстояния между Талгар и Юпитером
def calculate_distance(coord1, coord2):
    # Используем формулу гаверсинусов для расчета расстояния на сфере Земли
    R = 6371  # радиус Земли в км
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1 = lat1 * u.deg.to(u.rad)
    phi2 = lat2 * u.deg.to(u.rad)
    delta_phi = (lat2 - lat1) * u.deg.to(u.rad)
    delta_lambda = (lon2 - lon1) * u.deg.to(u.rad)

    a = (u.sin(delta_phi / 2))**2 + u.cos(phi1) * u.cos(phi2) * (u.sin(delta_lambda / 2))**2
    c = 2 * u.atan2(u.sqrt(a), u.sqrt(1 - a))

    distance = R * c
    return distance

# Шаг 4: Определение ингредиентов коктейля на основе расстояния
def get_cocktail_ingredients(distance):
    if distance < 5000:
        ingredients = ["Водка", "Лимонный сок", "Сахар"]
    elif distance < 10000:
        ingredients = ["Текила", "Ананасовый сок", "Кола"]
    else:
        ingredients = ["Виски", "Кофейный ликер", "Шоколадный сироп"]
    return ingredients

# Получаем координаты Юпитера
jupiter_ra, jupiter_dec = get_jupiter_geocentric_coordinates()

# Рассчитываем расстояние между Талгар и Юпитером
distance_to_jupiter = calculate_distance(talgar_coords, (jupiter_dec, jupiter_ra))

# Получаем ингредиенты коктейля
cocktail_ingredients = get_cocktail_ingredients(distance_to_jupiter)

print(f"Расстояние до Юпитера: {distance_to_jupiter:.2f} км")
print("Ингредиенты коктейля:", cocktail_ingredients)

# Шаг 5: Визуализация на карте
m = folium.Map(location=talgar_coords, zoom_start=10)
folium.Marker(talgar_coords, popup="Река Талгар").add_to(m)
folium.Marker([jupiter_dec, jupiter_ra], popup=f"Юпитер (расстояние: {distance_to_jupiter:.2f} км)").add_to(m)

# Сохранение карты
m.save("249.html")