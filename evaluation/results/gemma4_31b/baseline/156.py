import folium
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point

def generate_flood_risk_model():
    # 1. Координаты основных объектов (приблизительные для бассейна р. Или)
    # Или (основное русло), Сарыкан и Шынжалы (притоки)
    rivers_data = {
        'Ili': [[78.0, 42.0], [78.5, 42.5], [79.0, 43.0], [79.5, 43.5]],
        'Sarykan': [[78.2, 42.2], [78.4, 42.1], [78.6, 42.3]],
        'Shynzhaly': [[78.7, 42.6], [78.9, 42.5], [79.1, 42.7]]
    }

    # Создаем GeoDataFrame для рек
    river_lines = []
    for name, coords in rivers_data.items():
        # Переставляем координаты в формат (lon, lat) для LineString
        line = LineString(coords)
        river_lines.append({'name': name, 'geometry': line})
    
    gdf_rivers = gpd.GeoDataFrame(river_lines, crs="EPSG:4326")

    # 2. Симуляция сетки анализа (Grid) для оценки риска
    # Создаем сетку точек вокруг бассейна
    lat_range = np.linspace(42.0, 43.5, 20)
    lon_range = np.linspace(78.0, 79.5, 20)
    
    risk_zones = []
    
    for lat in lat_range:
        for lon in lon_range:
            p = Point(lon, lat)
            
            # Вычисляем минимальное расстояние до ближайшей реки (в градусах для упрощения)
            min_dist = min([p.distance(line) for line in gdf_rivers.geometry])
            
            # Имитация высоты (чем севернее и западнее, тем ниже - упрощенно)
            elevation = (lat - 42.0) * 100 + (lon - 78.0) * 50
            
            # Формула риска: Высокий риск если расстояние мало И высота низкая
            # Risk = (1/dist) * (1/elevation)
            risk_score = (1.0 / (min_dist + 0.1)) * (100 / (elevation + 10))
            
            # Классификация
            if risk_score > 15:
                level = 'High'
                color = 'red'
            elif risk_score > 7:
                level = 'Medium'
                color = 'orange'
            else:
                level = 'Low'
                color = 'green'
                
            risk_zones.append({'lat': lat, 'lon': lon, 'level': level, 'color': color, 'score': risk_score})

    # 3. Визуализация с помощью Folium
    m = folium.Map(location=[42.7, 78.7], zoom_start=8, tiles='CartoDB positron')

    # Добавляем реки на карту
    for idx, row in gdf_rivers.iterrows():
        coords = [[p[1], p[0]] for p in row.geometry.coords]
        folium.PolyLine(coords, color='blue', weight=4, opacity=0.8, 
                       tooltip=f"River: {row['name']}").add_to(m)

    # Добавляем зоны риска в виде кругов (Heatmap-like)
    for zone in risk_zones:
        folium.CircleMarker(
            location=[zone['lat'], zone['lon']],
            radius=5,
            color=zone['color'],
            fill=True,
            fill_color=zone['color'],
            fill_opacity=0.6,
            popup=f"Risk: {zone['level']} (Score: {zone['score']:.2f})"
        ).add_to(m)

    # Добавляем легенду
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 100px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Flood Risk Level</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> High Risk<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Medium Risk<br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Low Risk<br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> River Network
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("156.html")
    print("Modeling complete. Map saved as 156.html")

if __name__ == "__main__":
    generate_flood_risk_model()