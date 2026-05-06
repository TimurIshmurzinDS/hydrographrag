import folium
import pandas as pd
import numpy as np

def solve_drought_risk():
    # 1. Имитация пространственных данных (Координаты рек)
    # В реальном сценарии здесь был бы загрузкой GeoJSON или Shapefile
    rivers_data = {
        "Aksu River": {
            "coords": [[43.1, 81.2], [43.2, 81.4], [43.4, 81.6]], 
            "avg_precipitation": 150, # мм/год (низко)
            "evapotranspiration": 800, # мм/год (высоко)
            "farm_density": 0.8,       # коэффициент плотности хозяйств (высоко)
            "water_level_trend": -0.15 # тенденция снижения уровня воды
        },
        "Temirlik River": {
            "coords": [[43.5, 80.1], [43.6, 80.3], [43.8, 80.5]], 
            "avg_precipitation": 250, # мм/год (средне)
            "evapotranspiration": 600, # мм/год (средне)
            "farm_density": 0.4,       # коэффициент плотности хозяйств (средне)
            "water_level_trend": -0.05 # тенденция снижения уровня воды
        }
    }

    # 2. Расчет индекса риска засухи
    risk_results = {}
    
    for river, data in rivers_data.items():
        # Индекс засушливости (чем меньше отношение осадков к испарению, тем суше)
        aridity_index = data["avg_precipitation"] / data["evapotranspiration"]
        
        # Инвертируем индекс: чем меньше осадков относительно испарения, тем выше риск
        climate_risk = 1 / (aridity_index + 0.1) 
        
        # Итоговый риск = Климатический риск * Плотность ферм * Коэффициент падения уровня воды
        # Добавляем абсолютное значение тренда уровня воды
        total_risk = climate_risk * data["farm_density"] * (1 + abs(data["water_level_trend"]))
        risk_results[river] = total_risk

    # Определение реки с максимальным риском
    highest_risk_river = max(risk_results, key=risk_results.get)
    
    print(f"Calculated Risk Scores: {risk_results}")
    print(f"The river at higher risk of drought is: {highest_risk_river}")

    # 3. Визуализация с помощью folium
    # Центрируем карту в регионе (Центральная Азия)
    m = folium.Map(location=[43.5, 80.8], zoom_start=7, tiles="CartoDB positron")

    colors = {
        "Aksu River": "red" if highest_risk_river == "Aksu River" else "blue",
        "Temirlik River": "red" if highest_risk_river == "Temirlik River" else "blue"
    }

    for river, data in rivers_data.items():
        # Рисуем линию реки
        folium.PolyLine(
            locations=data["coords"], 
            color=colors[river], 
            weight=5, 
            opacity=0.8, 
            tooltip=f"{river} - Risk: {risk_results[river]:.2f}"
        ).add_to(m)
        
        # Добавляем маркеры для фермерских зон (буферы)
        for coord in data["coords"]:
            folium.Circle(
                location=coord,
                radius=20000, # 20 км зона влияния
                color=colors[river],
                fill=True,
                fill_opacity=0.2,
                popup=f"Farm Zone: {river}"
            ).add_to(m)

    # Добавление легенды через HTML
    legend_html = f'''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Drought Risk Legend</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> High Risk ({highest_risk_river})<br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Lower Risk
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("111.html")
    print("Map has been saved as 111.html")

if __name__ == "__main__":
    solve_drought_risk()