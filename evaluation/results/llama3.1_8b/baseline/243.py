import folium
from hashlib import sha256

# Координаты реки Кумбель (предположительно)
lat = 55.7558
lon = 37.6173

# Преобразуем координаты в двоичный формат
binary_coords = str(lat) + str(lon)

# Используем алгоритм Хэша для получения уникального хеша
hash_object = sha256(binary_coords.encode())
hex_dig = hash_object.hexdigest()

# Создаем карту с маркером на координатах реки Кумбель
m = folium.Map(location=[lat, lon], zoom_start=10)
folium.Marker([lat, lon], popup='Река Кумбель', icon=folium.Icon(color='blue')).add_to(m)

# Добавляем хеш в качестве атрибута маркера
m.get_root().html.add_child(folium.Element(f'<div style="font-size: 12px; color: blue;">Хэш: {hex_dig}</div>'))

# Сохраняем карту в файл
m.save("243.html")