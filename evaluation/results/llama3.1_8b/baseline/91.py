import folium
from folium.plugins import MarkerCluster

# Загрузите данные о реках из базы данных или файла.
# Для примера мы будем использовать фиксированные данные.
data = [
    {"name": "Уржар", "lat": 56.8, "lon": 60.0},
    {"name": "Печора", "lat": 65.1, "lon": 59.9},
    {"name": "Вишера", "lat": 61.2, "lon": 58.5},
    # Добавьте остальные реки...
]

# Производим фильтрацию данных, чтобы получить только притоки реки Уржар.
urzharsk_prityoki = [river for river in data if river["name"] != "Уржар"]

# Найдем координаты каждого притока и добавим их к данным.
for river in urzharsk_prityoki:
    river["lat"], river["lon"] = 56.7, 60.1  # примерные координаты

# Создаем интерактивную карту с маркерами для каждого притока.
m = folium.Map(location=[57.0, 59.5], zoom_start=8)

marker_cluster = MarkerCluster().add_to(m)
for river in urzharsk_prityoki:
    folium.Marker([river["lat"], river["lon"]], popup=f"{river['name']}").add_to(marker_cluster)

# Сохраняем карту в файл.
m.save("91.html")