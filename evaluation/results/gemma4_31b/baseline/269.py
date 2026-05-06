import folium
import random
import numpy as np

def generate_lunar_farm():
    # 1. Координаты "Лунной базы" (имитация координат на поверхности Луны)
    # Поскольку folium работает с земными координатами, мы используем 
    # определенный регион как проекцию лунной поверхности (например, район в пустыне или океане)
    # Для визуализации используем темную карту, чтобы имитировать космос.
    center_lat, center_lon = -89.5, 0.0  # Южный полюс (имитация района кратера Шеклтон)
    
    # Создаем карту с темным стилем
    m = folium.Map(location=[center_lat, center_lon], 
                   zoom_start=12, 
                   tiles='CartoDB dark_matter')

    # 2. Определение источника (Аналог реки Киши Осек - ледяной карьер)
    source_point = [center_lat, center_lon]
    folium.Marker(source_point, popup="Источник воды (Ледяной карьер Киши Осек-Луна)", 
                  icon=folium.Icon(color='blue', icon='tint')).add_to(m)

    # 3. Генерация магистрального канала (Main Irrigation Line)
    # Создаем путь от источника вглубь "фермы"
    main_line_coords = []
    current_lat, current_lon = center_lat, center_lon
    
    for i in range(5):
        main_line_coords.append([current_lat, current_lon])
        current_lat += random.uniform(0.01, 0.02)
        current_lon += random.uniform(-0.01, 0.01)
    
    main_line_coords.append([current_lat, current_lon])
    
    # Отрисовка магистрального канала
    folium.PolyLine(main_line_coords, color='cyan', weight=5, opacity=0.8, 
                    tooltip="Магистральный трубопровод Киши Осек").add_to(m)

    # 4. Создание распределительных сетей и ферм (Domes)
    # В каждой точке магистрали создаем ответвления к куполам
    for point in main_line_coords:
        # Создаем 2-3 фермы вокруг каждой точки магистрали
        for j in range(random.randint(2, 3)):
            offset_lat = random.uniform(-0.015, 0.015)
            offset_lon = random.uniform(-0.015, 0.015)
            farm_coords = [point[0] + offset_lat, point[1] + offset_lon]
            
            # Линия от магистрали к ферме (второстепенный канал)
            folium.PolyLine([point, farm_coords], color='lightblue', weight=2, opacity=0.6).add_to(m)
            
            # Купол фермы (Зона орошения)
            folium.Circle(
                location=farm_coords,
                radius=500, # 500 метров
                color='green',
                fill=True,
                fill_color='lime',
                fill_opacity=0.4,
                popup=f"Гидропонный модуль {random.randint(100, 999)}"
            ).add_to(m)

    # Добавляем легенду через HTML
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 250px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;">
     <b>Легенда Лунной Фермы:</b><br>
     <i style="color:blue">●</i> Источник (Лед)<br>
     <i style="color:cyan">━</i> Магистраль Киши Осек<br>
     <i style="color:lightblue">━</i> Распределительная сеть<br>
     <i style="color:lime">●</i> Купольная ферма
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("269.html")
    print("Модель успешно построена и сохранена в файл 269.html")

if __name__ == "__main__":
    generate_lunar_farm()