import folium
import numpy as np
import pandas as pd

def calculate_flood_risk(precipitation, temperature, slope_factor):
    """
    Симуляция расчета индекса риска паводка.
    precipitation: текущие осадки (мм)
    temperature: температура в горах (C)
    slope_factor: коэффициент крутизны рельефа (0.1 - 1.0)
    """
    # Весовые коэффициенты
    W_p = 0.5  # Осадки - главный фактор
    W_t = 0.3  # Таяние снегов
    W_s = 0.2  # Рельеф
    
    # Нормализация данных (условная)
    risk_score = (precipitation * W_p) + (temperature * W_t) + (slope_factor * 10 * W_s)
    
    if risk_score > 40:
        return "High", "red"
    elif risk_score > 20:
        return "Medium", "orange"
    else:
        return "Low", "green"

# 1. Координаты реки Большой Алматы (упрощенный маршрут от гор к городу)
river_coords = [
    [43.1500, 76.9500], # Верховья
    [43.1200, 76.9200],
    [43.0800, 76.8800],
    [43.0500, 76.8500],
    [43.0200, 76.8200]  # Нижний бьеф
]

# 2. Текущие параметры среды (Симуляция данных)
current_data = {
    "precipitation": 45,  # мм осадков за последние 24 часа
    "temperature": 12,    # градусы Цельсия в высокогорье
    "slope_factor": 0.8   # Высокий уклон (горная река)
}

# 3. Расчет риска
risk_level, risk_color = calculate_flood_risk(
    current_data["precipitation"], 
    current_data["temperature"], 
    current_data["slope_factor"]
)

# 4. Создание карты
m = folium.Map(location=[43.08, 76.88], zoom_start=11, tiles="CartoDB positron")

# Добавление линии реки
folium.PolyLine(
    locations=river_coords, 
    color="blue", 
    weight=4, 
    opacity=0.8, 
    tooltip="Ulken Almaty River"
).add_to(m)

# Создание зон риска (буферы вокруг точек реки)
for coord in river_coords:
    folium.Circle(
        location=coord,
        radius=1500, # Радиус потенциального затопления в метрах
        color=risk_color,
        fill=True,
        fill_color=risk_color,
        fill_opacity=0.4,
        popup=f"Risk Level: {risk_level}"
    ).add_to(m)

# Добавление информационного маркера
folium.Marker(
    location=river_coords[0],
    popup=f"Current Flood Risk: {risk_level}",
    icon=folium.Icon(color=risk_color, icon="info-sign")
).add_to(m)

# Добавление легенды через HTML
legend_html = f'''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Flood Risk Index</b><br>
     <i style="background:{risk_color}; width:10px; height:10px; display:inline-block"></i> {risk_level}
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("16.html")

print(f"Modeling complete. Current risk level: {risk_level}. Map saved as 16.html")