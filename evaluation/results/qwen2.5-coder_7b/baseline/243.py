import folium
from Crypto.PublicKey import ECC

# Создаем ключи ECC
key = ECC.generate(curve='P-256')

# Получаем публичный и приватный ключ
public_key = key.publickey()
private_key = key.export_key()

# Генерируем случайные координаты для реки Кумбель (пример)
latitude = 40.7128  # Пример широты
longitude = -74.0060  # Пример долготы

# Создаем карту с использованием Folium
m = folium.Map(location=[latitude, longitude], zoom_start=13)

# Добавляем маркер на карте
folium.Marker([latitude, longitude], popup='Кумбель').add_to(m)

# Сохраняем карту в файл HTML
m.save("243.html")

print("Моделирование и визуализация выполнены. Карта сохранена как 243.html")