import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
from scipy.spatial import distance

def generate_urzhar_risk_model():
    # 1. Симуляция геоданных (так как реальные shape-файлы отсутствуют)
    # Координаты реки Уржар (приблизительная область в Казахстане)
    river_coords = [
        [47.5, 62.0], [47.6, 62.2], [47.8, 62.5], 
        [48.0, 62.8], [48.2, 63.0], [48.5, 63.2]
    ]
    
    # Создаем сетку точек вокруг реки для анализа (имитация участков полей)
    lats = np.linspace(47.3, 48.7, 30)
    lons = np.linspace(61.8, 63.4, 30)
    grid_points = []
    for lat in lats:
        for lon in lons:
            grid_points.append([lat, lon])
    
    # 2. Моделирование факторов риска
    data = []
    river_pts = np.array(river_coords)
    
    for pt in grid_points:
        # А. Расстояние до реки (чем ближе, тем выше риск - инвертируем)
        # Вычисляем минимальное расстояние до любой точки реки
        dist_to_river = np.min([distance.euclidean(pt, r) for r in river_coords])
        # Нормализация: близко (0.1) -> высокий риск (1.0), далеко -> низкий риск (0.0)
        norm_dist = np.exp(-dist_to_river * 5) 
        
        # Б. Уклон (имитация: в низинах у реки уклон меньше)
        # Генерируем случайный уклон, но делаем его меньше вблизи реки
        slope = np.random.uniform(0, 10) - (norm_dist * 5)
        slope = max(0, slope)
        # Нормализация: малый уклон -> высокий риск
        norm_slope = 1.0 / (1.0 + slope)
        
        # В. Тип почвы (имитация: случайное распределение проницаемости)
        # 0: песчаные (низкий риск), 1: глинистые (высокий риск)
        soil_type_risk = np.random.choice([0.2, 0.5, 0.9], p=[0.3, 0.4, 0.3])
        
        # 3. Расчет итогового индекса риска (WLC)
        # Веса: Дистанция (40%), Уклон (30%), Почва (30%)
        sri = (norm_dist * 0.4) + (norm_slope * 0.3) + (soil_type_risk * 0.3)
        
        data.append({
            'lat': pt[0],
            'lon': pt[1],
            'risk': sri
        })

    df = pd.DataFrame(data)

    # 4. Визуализация с помощью folium
    # Центр карты
    m = folium.Map(location=[48.0, 62.5], zoom_start=8, tiles='OpenStreetMap')

    # Добавляем линию реки
    folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Река Уржар").add_to(m)

    # Добавляем точки риска
    for _, row in df.iterrows():
        # Определяем цвет в зависимости от уровня риска
        if row['risk'] < 0.3:
            color = 'green'
            popup = 'Низкий риск'
        elif row['risk'] < 0.6:
            color = 'orange'
            popup = 'Средний риск'
        else:
            color = 'red'
            popup = 'Высокий риск'
            
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"Риск: {row['risk']:.2f} ({popup})"
        ).add_to(m)

    # Добавляем тепловую карту для общего понимания зон
    heat_data = [[row['lat'], row['lon'], row['risk']] for index, row in df.iterrows()]
    HeatMap(heat_data, radius=15, blur=20).add_to(m)

    # Сохранение карты
    m.save("195.html")
    print("Modeling complete. Map saved as 195.html")

if __name__ == "__main__":
    generate_urzhar_risk_model()