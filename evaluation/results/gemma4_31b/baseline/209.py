import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
import random

def simulate_urzhar_basin_flood():
    # 1. Определение координат бассейна реки Уржар (приблизительные границы)
    # Центр бассейна в Казахстане
    center_lat, center_lon = 47.5, 68.5 
    grid_size = 20  # Размер сетки для симуляции (20x20 точек)
    
    # Создаем сетку координат
    lat_range = np.linspace(center_lat - 0.5, center_lat + 0.5, grid_size)
    lon_range = np.linspace(center_lon - 0.5, center_lon + 0.5, grid_size)
    
    data = []
    
    # 2. Симуляция геопространственных параметров
    # В реальном проекте здесь загружаются GeoTIFF файлы (DEM, Precipitation)
    for lat in lat_range:
        for lon in lon_range:
            # Симулируем высоту (DEM): чем ближе к центру/реке, тем ниже
            dist_from_center = np.sqrt((lat - center_lat)**2 + (lon - center_lon)**2)
            elevation = 150 + (dist_from_center * 100) + random.uniform(-10, 10)
            
            # Симулируем экстремальные осадки (мм)
            # Создаем "ядро" шторма в определенной части бассейна
            precipitation = 100 + (50 * np.exp(-( (lat-47.6)**2 + (lon-68.6)**2 ) / 0.1))
            
            # Коэффициент стока (зависит от почвы, упрощенно 0.3 - 0.7)
            runoff_coeff = random.uniform(0.3, 0.7)
            
            # 3. Расчет индекса риска наводнения (FRI)
            # Риск выше там, где: много осадков, высокий сток и низкая высота
            # Формула: (Осадки * Сток) / (Высота * 0.1)
            risk_score = (precipitation * runoff_coeff) / (elevation * 0.1)
            
            data.append([lat, lon, risk_score])

    # Преобразование в DataFrame
    df = pd.DataFrame(data, columns=['lat', 'lon', 'risk'])

    # 4. Визуализация с помощью Folium
    # Создаем карту
    m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles='OpenStreetMap')

    # Добавляем тепловую карту рисков
    # HeatMap принимает список [lat, lon, weight]
    heat_data = df[['lat', 'lon', 'risk']].values.tolist()
    HeatMap(heat_data, radius=15, blur=10, min_opacity=0.5).add_to(m)

    # Добавляем маркеры для зон критического риска (верхние 5% значений)
    threshold = df['risk'].quantile(0.95)
    critical_zones = df[df['risk'] >= threshold]

    for idx, row in critical_zones.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"High Risk: {row['risk']:.2f}"
        ).add_to(m)

    # Сохранение карты
    m.save("209.html")
    print("Modeling complete. Map saved as 209.html")

if __name__ == "__main__":
    simulate_urzhar_basin_flood()