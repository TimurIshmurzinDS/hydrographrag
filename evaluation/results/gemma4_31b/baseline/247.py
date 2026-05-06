import folium
from shapely.geometry import LineString, Point, Polygon

# 1. Симуляция геоданных реки Каскелен и её притоков
# Координаты приблизительно соответствуют региону реки Каскелен (Казахстан)
kaskelen_main_river = [
    [43.15, 77.10], [43.12, 77.15], [43.08, 77.20], [43.05, 77.25], [43.00, 77.30]
]

tributaries = {
    "Tributary_A": [[43.14, 77.05], [43.13, 77.11]],
    "Tributary_B": [[43.10, 77.12], [43.09, 77.16]],
    "Tributary_C": [[43.06, 77.22], [43.06, 77.26]],
}

# 2. Функция для создания буферной зоны (имитация зоны охлаждения)
def create_cooling_buffer(coords, radius=0.01):
    # В реальном ГИС используется geopandas.buffer, здесь упрощенная имитация для folium
    buffer_points = []
    for lat, lon in coords:
        buffer_points.append([lat + radius, lon + radius])
    buffer_points.append([coords[-1][0] - radius, coords[-1][1] - radius])
    buffer_points.append([coords[0][0] - radius, coords[0][1] - radius])
    return buffer_points

# 3. Инициализация карты
m = folium.Map(location=[43.08, 77.20], zoom_start=10, tiles="CartoDB positron")

# 4. Визуализация основного русла
main_line = folium.PolyLine(kaskelen_main_river, color="blue", weight=5, opacity=0.8, tooltip="Река Каскелен (Основное русло)")
m.add_layer(main_line)

# 5. Визуализация притоков и расчет "Майнинг-хабов"
mining_sites = []

for name, coords in tributaries.items():
    # Рисуем приток
    folium.PolyLine(coords, color="lightblue", weight=3, opacity=0.6, tooltip=name).add_to(m)
    
    # Создаем зону охлаждения вокруг притока
    buffer_zone = create_cooling_buffer(coords)
    folium.Polygon(buffer_zone, color="cyan", fill=True, fill_opacity=0.2, tooltip=f"Зона охлаждения {name}").add_to(m)
    
    # Точка слияния (конец притока) считается оптимальным местом для майнинга
    confluence_point = coords[-1]
    mining_sites.append(confluence_point)

# 6. Размещение майнинг-ферм в точках слияния
for i, site in enumerate(mining_sites):
    folium.Marker(
        location=site,
        popup=f"Mining Site #{i+1}: Высокий потенциал охлаждения",
        icon=folium.Icon(color="green", icon="bolt", prefix="fa")
    ).add_to(m)

# Добавление легенды через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 250px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда моделирования:</b><br>
     <i style="color:blue">━</i> Основная река<br>
     <i style="color:lightblue">━</i> Притоки<br>
     <i style="color:cyan">■</i> Зоны гидро-охлаждения<br>
     <i style="color:green">●</i> Оптимальные точки майнинга
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("247.html")

print("Modeling complete. The map has been saved as 247.html")