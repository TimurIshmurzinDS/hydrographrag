import folium
import geopandas as gpd
from shapely.geometry import LineString, Polygon
import numpy as np

def generate_river_risk_map():
    # 1. Имитация координат рек (Lepsy и Shynzhaly)
    # В реальном проекте здесь будет загрузка shape-файлов: gpd.read_file('rivers.shp')
    lepsy_coords = [
        (44.1, 78.5), (44.2, 78.7), (44.3, 78.9), (44.5, 79.1), (44.7, 79.3)
    ]
    shynzhaly_coords = [
        (44.0, 78.2), (44.1, 78.3), (44.2, 78.4), (44.3, 78.5), (44.4, 78.6)
    ]

    lepsy_line = LineString(lepsy_coords)
    shynzhaly_line = LineString(shynzhaly_coords)

    rivers = {
        "Lepsy River": lepsy_line,
        "Shynzhaly River": shynzhaly_line
    }

    # Создание карты, центрированной в регионе
    m = folium.Map(location=[44.3, 78.7], zoom_start=8, tiles='OpenStreetMap')

    # Цвета для уровней риска
    risk_colors = {
        "High": "red",
        "Medium": "orange",
        "Low": "yellow"
    }

    # 2. Моделирование зон риска (имитация анализа ЦМР)
    # Мы создаем буферы разного радиуса, которые представляют собой зоны потенциального затопления
    # В реальности радиус зависел бы от уклона (Slope) и высоты (Elevation)
    for name, line in rivers.items():
        # Отрисовка самой реки
        folium.PolyLine(
            locations=[(lat, lon) for lon, lat in line.coords], 
            color="blue", weight=4, opacity=0.8, tooltip=name
        ).add_to(m)

        # Создаем имитацию зон риска через буферизацию
        # High Risk: 0-2 км от реки (низменности)
        # Medium Risk: 2-5 км
        # Low Risk: 5-10 км
        
        # Для визуализации в folium мы создаем упрощенные полигоны вокруг линий
        # В реальном GIS это делается через Raster-to-Vector или Buffer в проекции UTM
        
        # Имитация зон (упрощенно через создание расширенных линий/полигонов)
        # Мы создаем "коридоры" риска
        for risk_level, width, color in [("Low", 0.1, "yellow"), ("Medium", 0.05, "orange"), ("High", 0.02, "red")]:
            # Создаем имитацию зоны риска вокруг реки
            # В данном примере мы просто рисуем линии разной толщины для наглядности 
            # или создаем небольшие смещения для имитации полигона
            folium.PolyLine(
                locations=[(lat, lon) for lon, lat in line.coords],
                color=color, 
                weight=width * 1000, # Масштабируем для визуального эффекта
                opacity=0.4, 
                tooltip=f"{risk_level} Risk Zone - {name}"
            ).add_to(m)

    # Добавление легенды
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Риск перелива:</b><br>
     <i style="background:red;width:10px;height:10px;display:inline-block"></i> Высокий<br>
     <i style="background:orange;width:10px;height:10px;display:inline-block"></i> Средний<br>
     <i style="background:yellow;width:10px;height:10px;display:inline-block"></i> Низкий<br>
     <i style="background:blue;width:10px;height:10px;display:inline-block"></i> Русло реки
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("159.html")
    print("Analysis complete. Map saved as 159.html")

if __name__ == "__main__":
    generate_river_risk_map()