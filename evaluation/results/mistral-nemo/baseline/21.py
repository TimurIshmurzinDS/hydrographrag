import folium

# Загрузите данные о сезонном расходе воды и их местоположение
data = [
    {"location": [latitude, longitude], "flow_rate": flow_rate}
    # Пример данных: [{'location': [49.2167, 28.4333], 'flow_rate': 500}, ...]
]

# Создайте геоданные (геопoints) из этих данных
geodata = [(d['location'][0], d['location'][1]) for d in data]

# Создайте карту с центром над местоположением реки Shyzhyn River
m = folium.Map(location=[49.2167, 28.4333], zoom_start=8)

# Добавьте геопoints на карту и добавьте информацию о сезонном расходе воды в виде всплывающих подсказок
for point in geodata:
    folium.CircleMarker(location=point, radius=5).add_to(m)
    folium.Marker(point, popup=f"Сезонный расход воды: {data[geodata.index(point)]['flow_rate']} куб. м/с").add_to(m)

# Сохраните финальную карту как "21.html"
m.save("21.html")