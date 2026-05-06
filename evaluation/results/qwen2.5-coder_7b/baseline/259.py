import folium
from geopy.geocoders import Nominatim

# Определение местоположения реки Баскан
geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.geocode("Баскан, Россия")

if location:
    bascan_location = (location.latitude, location.longitude)
else:
    print("Не удалось определить местоположение реки Баскан.")
    exit()

# Оценка доступности воды
water_volume_required = 1000  # Пример: требуется 1000 литров воды для охлаждения двигателей
bascan_water_volume = 50000  # Пример: объем воды в реке Баскан

if bascan_water_volume >= water_volume_required:
    print("Достаточно воды в реке Баскан для охлаждения двигателей.")
else:
    print("Недостаточно воды в реке Баскан для охлаждения двигателей.")

# Оценка влияния на окружающую среду
if bascan_water_volume >= water_volume_required * 2:
    print("Использование воды из реки Баскан не будет иметь значительного влияния на окружающую среду.")
else:
    print("Использование воды из реки Баскан может негативно влиять на окружающую среду.")

# Визуализация местоположения реки Баскан
m = folium.Map(location=bascan_location, zoom_start=12)
folium.Marker(bascan_location, popup='Река Баскан').add_to(m)

# Сохранение карты
m.save("259.html")