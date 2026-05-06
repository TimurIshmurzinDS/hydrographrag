import folium
import geopandas as gpd
from shapely.geometry import LineString, Point

def analyze_flood_zones():
    # 1. Координаты рек (имитация геометрии русел для Shyzhyn и Sarykan)
    # В реальном проекте здесь будет загрузка из GeoJSON или Shapefile
    rivers_data = {
        "Shyzhyn River": [
            (48.50, 68.10), (48.52, 68.15), (48.55, 68.20), (48.58, 68.25)
        ],
        "Sarykan River": [
            (48.60, 68.30), (48.63, 68.35), (48.67, 68.40), (48.70, 68.45)
        ]
    }

    # Создаем карту, центрированную в регионе
    m = folium.Map(location=[48.60, 68.25], zoom_start=10, tiles="CartoDB positron")

    # Цвета для уровней риска
    # Красный: Высокий риск (близко к руслу), Желтый: Средний риск (пойма)
    risk_levels = [
        {"width": 0.005, "color": "red", "label": "High Risk Zone"},
        {"width": 0.015, "color": "orange", "label": "Medium Risk Zone"},
        {"width": 0.030, "color": "yellow", "label": "Low Risk Zone"}
    ]

    for river_name, coords in rivers_data.items():
        # Создаем линию реки
        river_line = LineString(coords)
        
        # Добавляем саму реку на карту
        folium.PolyLine(
            coords, 
            color="blue", 
            weight=4, 
            opacity=0.8, 
            tooltip=f"River: {river_name}"
        ).add_to(m)

        # Имитация моделирования зон затопления через создание буферов
        # В реальном GIS это делается через анализ DEM (HAND model)
        for risk in risk_levels:
            # Создаем упрощенный буфер вокруг каждой точки линии
            for point in coords:
                folium.Circle(
                    location=point,
                    radius=risk["width"] * 100000, # Конвертация условных единиц в метры
                    color=risk["color"],
                    fill=True,
                    fill_opacity=0.3,
                    popup=f"{river_name}: {risk['label']}"
                ).add_to(m)

    # Добавление легенды через HTML
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Flood Risk Legend</b><br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> River Bed<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> High Risk<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Medium Risk<br>
     <i style="background:yellow; width:10px; height:10px; display:inline-block"></i> Low Risk
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение результата
    m.save("165.html")
    print("Analysis complete. Map saved as 165.html")

if __name__ == "__main__":
    analyze_flood_zones()