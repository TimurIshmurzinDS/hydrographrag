import folium
import pandas as pd
import numpy as np
import random

# 1. Симуляция данных для речных экосистем
# Координаты (приблизительные центры бассейнов)
# Шарын: ~43.5, 79.5 | Уржар: ~49.5, 82.5
def generate_river_data(river_name, lat_center, lon_center, num_points=15):
    data = []
    for i in range(num_points):
        # Создаем случайные точки вокруг центра бассейна
        lat = lat_center + random.uniform(-1.5, 1.5)
        lon = lon_center + random.uniform(-1.5, 1.5)
        
        # Симулируем экологические показатели
        # Для Шарына (засушливый регион) WQI может быть ниже из-за минерализации
        # Для Уржара показатели могут отличаться в зависимости от антропогенной нагрузки
        if river_name == "Sharyn":
            wqi = random.randint(40, 80)
            ndvi = random.uniform(0.2, 0.5)
        else: # Urzhar
            wqi = random.randint(50, 90)
            ndvi = random.uniform(0.3, 0.7)
            
        status = "Good" if wqi > 70 else "Fair" if wqi > 50 else "Poor"
        
        data.append({
            "River": river_name,
            "Lat": lat,
            "Lon": lon,
            "WQI": wqi,
            "NDVI": ndvi,
            "Status": status
        })
    return data

# Генерация датасетов
sharyn_data = generate_river_data("Sharyn", 43.5, 79.5)
urzhar_data = generate_river_data("Urzhar", 49.5, 82.5)
df = pd.DataFrame(sharyn_data + urzhar_data)

# 2. Сравнительный анализ
summary = df.groupby('River').agg({
    'WQI': 'mean',
    'NDVI': 'mean'
}).reset_index()

print("--- Сравнительный анализ экологического статуса ---")
print(summary)

# 3. Визуализация на карте
# Создаем карту с центром в Казахстане
m = folium.Map(location=[45.0, 82.0], zoom_start=5, tiles='CartoDB positron')

# Функция для определения цвета маркера
def get_color(status):
    if status == "Good":
        return 'green'
    elif status == "Fair":
        return 'orange'
    else:
        return 'red'

# Добавление точек мониторинга на карту
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=7,
        popup=f"River: {row['River']}<br>WQI: {row['WQI']}<br>NDVI: {row['NDVI']:.2f}<br>Status: {row['Status']}",
        color=get_color(row['Status']),
        fill=True,
        fill_color=get_color(row['Status']),
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Экологический статус:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Хороший<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Удовлетворительный<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Плохой
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("188.html")
print("\nКарта успешно сохранена в файл 188.html")