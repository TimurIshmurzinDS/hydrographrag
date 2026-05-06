import folium
import pandas as pd
import numpy as np
import random

def generate_sarykan_basin_data():
    """
    Симуляция данных гидрографической сети бассейна реки Сарыкан.
    В реальном проекте здесь будет загрузка Shape-файлов или GeoJSON.
    """
    # Координаты центральной части бассейна (примерные для региона)
    center_lat, center_lon = 48.5, 62.0 
    
    rivers = [
        {"name": "Sarykan Main Stem", "segments": 10, "base_risk": 0.6},
        {"name": "Tributary A", "segments": 5, "base_risk": 0.4},
        {"name": "Tributary B", "segments": 5, "base_risk": 0.8},
        {"name": "Tributary C", "segments": 5, "base_risk": 0.3},
        {"name": "Tributary D", "segments": 5, "base_risk": 0.7},
    ]
    
    river_data = []
    for river in rivers:
        # Генерируем случайные координаты для сегментов реки
        start_lat = center_lat + random.uniform(-0.5, 0.5)
        start_lon = center_lon + random.uniform(-0.5, 0.5)
        
        for i in range(river["segments"]):
            # Симуляция факторов риска для каждого сегмента
            slope_factor = random.uniform(0, 1) # 0 - крутой, 1 - плоский
            soil_factor = random.uniform(0, 1)  # 0 - песчаный, 1 - глинистый
            precip_factor = random.uniform(0, 1) # интенсивность таяния
            
            # Расчет FSI (Flood Susceptibility Index)
            fsi = (slope_factor * 0.4) + (soil_factor * 0.3) + (precip_factor * 0.3)
            # Корректировка базовым риском реки
            final_risk = (fsi + river["base_risk"]) / 2
            
            # Координаты сегмента (линия)
            end_lat = start_lat + random.uniform(-0.05, 0.05)
            end_lon = start_lon + random.uniform(-0.05, 0.05)
            
            river_data.append({
                "river_name": river["name"],
                "coords": [[start_lat, start_lon], [end_lat, end_lon]],
                "risk_score": final_risk
            })
            start_lat, start_lon = end_lat, end_lon
            
    return river_data

def get_color(risk):
    """Определение цвета в зависимости от уровня риска"""
    if risk > 0.7:
        return 'red'    # Высокий риск
    elif risk > 0.4:
        return 'orange' # Средний риск
    else:
        return 'green'  # Низкий риск

def main():
    # 1. Получение данных
    data = generate_sarykan_basin_data()
    
    # 2. Создание карты
    # Центрируем карту на среднем значении координат
    m = folium.Map(location=[48.5, 62.0], zoom_start=7, tiles='CartoDB positron')
    
    # 3. Добавление рек на карту
    for segment in data:
        color = get_color(segment["risk_score"])
        
        folium.PolyLine(
            locations=segment["coords"],
            color=color,
            weight=4,
            opacity=0.8,
            tooltip=f"River: {segment['river_name']} | Risk: {segment['risk_score']:.2f}"
        ).add_to(m)
    
    # 4. Добавление легенды
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 160px; height: 90px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; opacity: 0.8; padding: 10px;">
    <b>Риск половодья:</b><br>
    <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий<br>
    <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний<br>
    <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # 5. Сохранение результата
    m.save("153.html")
    print("Modeling complete. Map saved as 153.html")

if __name__ == "__main__":
    main()