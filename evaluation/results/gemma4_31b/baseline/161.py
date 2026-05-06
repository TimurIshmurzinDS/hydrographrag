import folium
import numpy as np
from folium.plugins import HeatMap

def generate_flood_potential():
    # 1. Координаты примерных центров бассейнов рек (Казахстан, регион Жетысу/Алматинская обл.)
    # Shilik River и Shynzhaly River
    rivers_coords = {
        "Shilik": [43.5, 81.5], 
        "Shynzhaly": [43.8, 80.2]
    }

    # Создаем базовую карту
    m = folium.Map(location=[43.6, 80.8], zoom_start=8, tiles="CartoDB dark_matter")

    # 2. Симуляция моделирования зон затопления
    # В реальном GIS мы бы использовали растр ЦМР. Здесь мы создаем сетку точек 
    # вокруг рек и рассчитываем "индекс риска" на основе расстояния и случайного рельефа.
    
    flood_data = []

    for river_name, center in rivers_coords.items():
        # Генерируем сетку точек вокруг каждой реки для имитации бассейна
        for lat in np.linspace(center[0] - 0.5, center[0] + 0.5, 50):
            for lon in np.linspace(center[1] - 0.5, center[1] + 0.5, 50):
                
                # Имитация расстояния до русла (чем ближе, тем выше риск)
                dist_to_river = np.sqrt((lat - center[0])**2 + (lon - center[1])**2)
                
                # Имитация HAND (Height Above Nearest Drainage) 
                # Добавляем случайный шум, чтобы имитировать перепады высот
                hand_value = dist_to_river * np.random.uniform(0.5, 1.5)
                
                # Расчет потенциала затопления (Inverse relationship with HAND)
                # Риск высок, если HAND мал и расстояние до реки невелико
                risk_score = np.exp(-hand_value * 5) * 100 
                
                if risk_score > 5:  # Сохраняем только значимые зоны риска
                    flood_data.append([lat, lon, risk_score])

    # 3. Визуализация через HeatMap (Тепловая карта рисков)
    # Формат HeatMap: [[lat, lon, weight], ...]
    heat_data = [[point[0], point[1], point[2]] for point in flood_data]
    HeatMap(heat_data, radius=15, blur=20, min_opacity=0.3).add_to(m)

    # 4. Добавление маркеров рек
    for river_name, coords in rivers_coords.items():
        folium.Marker(
            location=coords,
            popup=f"Basin of {river_name} River",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # Добавление легенды (текстовое описание)
    title_html = '''
                 <div style="position: fixed; 
                             top: 50px; left: 50px; width: 300px; height: 90px; 
                             z-index:9999; font-size:14px; background-color:white;
                             padding: 10px; border: 2px solid black;">
                 <b>Оценка паводкового потенциала</b><br>
                 Красные зоны: Высокий риск (низкий HAND)<br>
                 Синие зоны: Низкий риск / Высоты<br>
                 Объекты: Бассейны р. Шилик и р. Шынгжалы
                 </div>
                 '''
    m.get_root().html.add_child(folium.Element(title_html))

    # Сохранение результата
    m.save("161.html")
    print("Modeling complete. Map saved as 161.html")

if __name__ == "__main__":
    generate_flood_potential()