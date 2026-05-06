import folium
from folium.plugins import HeatMap

# Сбор данных о реке Шынжалы
data = {
    'coordinates': [(46.123, 47.456), (46.234, 47.567)],
    'water_quality': [8.5, 9.2],
    'soil_quality': [7.1, 6.8],
    'air_quality': [4.3, 5.1]
}

# Создание геообъекта для реки Шынжалы
m = folium.Map(location=[46.179, 47.467], zoom_start=12)

# Визуализация экологических показателей на карте
folium.Marker([46.123, 47.456], popup='Вода: ' + str(data['water_quality'][0]) + ', Почва: ' + str(data['soil_quality'][0]) + ', Воздух: ' + str(data['air_quality'][0])).add_to(m)
folium.Marker([46.234, 47.567], popup='Вода: ' + str(data['water_quality'][1]) + ', Почва: ' + str(data['soil_quality'][1]) + ', Воздух: ' + str(data['air_quality'][1])).add_to(m)

# Визуализация результатов на карте
HeatMap(data['coordinates'], radius=10, max_val=max(data['water_quality'])).add_to(m)

# Сохранение карты в файл
m.save("44.html")