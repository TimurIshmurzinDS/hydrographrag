import folium
import numpy as np
import pandas as pd
import random

def generate_river_coords(start_coord, length=10, points=20):
    """Генерирует синтетические координаты русла реки"""
    coords = []
    curr_lat, curr_lon = start_coord
    for i in range(points):
        curr_lat += random.uniform(-0.01, 0.01)
        curr_lon += random.uniform(-0.02, 0.02)
        coords.append([curr_lat, curr_lon])
    return coords

def calculate_flood_probability(river_name):
    """
    Симуляция расчета вероятности наводнения.
    В реальном GIS это был бы расчет TWI + анализ осадков.
    """
    # Имитируем разные характеристики для двух рек
    if river_name == "Shynzhaly":
        # Допустим, Shynzhaly протекает по более плоской местности (выше риск)
        base_risk = np.random.uniform(0.6, 0.8)
    else:
        # Shyzhyn имеет более крутой уклон (ниже риск)
        base_risk = np.random.uniform(0.3, 0.5)
    
    # Добавляем случайную вариативность по длине реки
    risk_profile = [base_risk + np.random.uniform(-0.1, 0.1) for _ in range(20)]
    return risk_profile

# 1. Инициализация данных
rivers_data = {
    "Shynzhaly": {"start": [43.5, 65.0], "color": "blue"},
    "Shyzhyn": {"start": [43.6, 65.2], "color": "green"}
}

# 2. Создание карты
m = folium.Map(location=[43.55, 65.1], zoom_start=10, tiles="CartoDB positron")

results = {}

for name, info in rivers_data.items():
    # Генерируем геометрию реки
    coords = generate_river_coords(info["start"])
    # Рассчитываем вероятность наводнения для каждой точки русла
    probs = calculate_flood_probability(name)
    
    avg_prob = np.mean(probs)
    results[name] = avg_prob
    
    # Визуализация русла реки
    # Цвет линии зависит от среднего риска: красный если > 0.5, синий если < 0.5
    line_color = "red" if avg_prob > 0.5 else "blue"
    
    folium.PolyLine(
        coords, 
        color=line_color, 
        weight=5, 
        opacity=0.8, 
        tooltip=f"River: {name} | Avg Flood Prob: {avg_prob:.2f}"
    ).add_to(m)
    
    # Добавляем маркеры для точек с максимальным риском
    max_risk_idx = np.argmax(probs)
    folium.CircleMarker(
        location=coords[max_risk_idx],
        radius=7,
        color="darkred",
        fill=True,
        fill_color="darkred",
        popup=f"Critical Point {name}: Risk {probs[max_risk_idx]:.2f}"
    ).add_to(m)

# 3. Добавление легенды/информации через HTML
info_text = f"""
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 250px; height: 100px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                padding: 10px;">
    <b>Flood Probability Analysis:</b><br>
    Shynzhaly: {results['Shynzhaly']:.2f}<br>
    Shyzhyn: {results['Shyzhyn']:.2f}<br>
    <i>Higher value = Higher Risk</i>
    </div>
"""
m.get_root().html.add_child(folium.Element(info_text))

# Сохранение результата
m.save("154.html")

print("Modeling complete. Comparison results:")
for river, prob in results.items():
    print(f"{river}: {prob:.2f}")