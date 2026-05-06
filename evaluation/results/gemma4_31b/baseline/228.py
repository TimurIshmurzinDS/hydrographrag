import folium
import numpy as np

def generate_rocket_site_map():
    # 1. Координаты реки Аягоз (упрощенная аппроксимация русла для моделирования)
    # Река Аягоз протекает в Казахстане.
    river_coords = [
        [48.8500, 79.1000],
        [48.8300, 79.2000],
        [48.8100, 79.3500],
        [48.7800, 79.5000],
        [48.7500, 79.6500],
        [48.7200, 79.8000]
    ]

    # Создаем карту, центрированную на регионе
    m = folium.Map(location=[48.8000, 79.4000], zoom_start=9, tiles='CartoDB positron')

    # 2. Визуализация русла реки
    folium.PolyLine(river_coords, color="blue", weight=4, opacity=0.8, tooltip="Река Аягоз").add_to(m)

    # 3. Моделирование сезонных изменений через буферные зоны
    # В folium нет встроенного анализа буферов (как в ArcGIS/QGIS), 
    # поэтому мы имитируем зоны паводка с помощью полигонов вокруг линии.
    
    def create_buffer_polygon(coords, width_deg):
        """Создает упрощенный полигон-буфер вокруг линии"""
        buffer_points_left = []
        buffer_points_right = []
        
        for p in coords:
            # Смещение по долготе для имитации ширины реки/паводка
            buffer_points_left.append([p[0], p[1] - width_deg])
            buffer_points_right.append([p[0], p[1] + width_deg])
            
        # Соединяем точки в один замкнутый полигон
        polygon_coords = buffer_points_left[::-1] + buffer_points_right
        return polygon_coords

    # Зона весеннего паводка (High Water Level) - Красная зона (Опасно)
    flood_zone_coords = create_buffer_polygon(river_coords, 0.05)
    folium.Polygon(
        locations=flood_zone_coords,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.3,
        tooltip="Зона сезонного паводка (Запрещено строительство)"
    ).add_to(m)

    # Зона технического доступа (Safe Industrial Zone) - Зеленая зона
    # Это область, где мы можем строить: достаточно близко к воде, но выше уровня паводка
    access_zone_coords = create_buffer_polygon(river_coords, 0.12)
    folium.Polygon(
        locations=access_zone_coords,
        color="green",
        fill=False,
        weight=2,
        dash_array='5, 5',
        tooltip="Зона допустимого строительства"
    ).add_to(m)

    # 4. Определение точки строительства ракеты
    # Выбираем точку, которая находится в зеленой зоне, но вне красной
    rocket_site = [48.8000, 79.4500] 
    
    folium.Marker(
        location=rocket_site,
        popup="Место строительства ракеты",
        icon=folium.Icon(color="darkblue", icon="rocket", prefix="fa")
    ).add_to(m)

    # Добавляем легенду через HTML
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 250px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда моделирования:</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Зона паводка (Риск)<br>
     <i style="border:1px dashed green; width:10px; height:10px; display:inline-block"></i> Зона пригодности<br>
     <i style="color:blue; font-size:16px"></i> 🚀 Место застройки
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение результата
    m.save("228.html")
    print("Modeling complete. Map saved as 228.html")

if __name__ == "__main__":
    generate_rocket_site_map()