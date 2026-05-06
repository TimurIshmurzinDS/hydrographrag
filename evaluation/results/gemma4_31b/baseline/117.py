import pandas as pd
import numpy as np
import folium
from folium.plugins import PolyLineTextPath

# 1. Симуляция геоданных для рек Уржар и Аксу
# Координаты (приблизительные для демонстрации методологии)
rivers_data = {
    "Urzhar": [
        [47.5, 68.2], [47.6, 68.5], [47.8, 68.8], [48.0, 69.1]
    ],
    "Aksu": [
        [46.2, 70.1], [46.5, 70.4], [46.8, 70.7], [47.1, 71.0]
    ]
}

# 2. Симуляция временных рядов (Сток и NDVI)
# Создаем данные: Год, Река, Средний сток (м3/с), Средний NDVI
np.random.seed(42)
years = np.arange(2014, 2024)
data_list = []

for river in ["Urzhar", "Aksu"]:
    # Симулируем постепенное снижение стока
    base_flow = 15 if river == "Urzhar" else 25
    flow = base_flow - (np.arange(10) * 0.5) + np.random.normal(0, 1, 10)
    
    # Симулируем NDVI, который коррелирует со стоком (снижение стока -> снижение NDVI)
    ndvi = 0.6 - (np.arange(10) * 0.02) + np.random.normal(0, 0.03, 10)
    
    for i in range(10):
        data_list.append({
            "Year": years[i],
            "River": river,
            "Flow": flow[i],
            "NDVI": ndvi[i]
        })

df = pd.DataFrame(data_list)

# 3. Анализ дисбаланса
def calculate_imbalance(river_name):
    river_df = df[df['River'] == river_name]
    
    # Рассчитываем изменение стока (последний год vs первый)
    flow_change = (river_df['Flow'].iloc[-1] - river_df['Flow'].iloc[0]) / river_df['Flow'].iloc[0]
    # Рассчитываем изменение NDVI
    ndvi_change = (river_df['NDVI'].iloc[-1] - river_df['NDVI'].iloc[0])
    
    # Критерий дисбаланса: если сток упал более чем на 10% и NDVI снизился
    if flow_change < -0.1 and ndvi_change < 0:
        return "High Imbalance", "red"
    elif flow_change < -0.05:
        return "Moderate Imbalance", "orange"
    else:
        return "Stable", "green"

# 4. Визуализация на карте
m = folium.Map(location=[47.0, 69.0], zoom_start=6, tiles="CartoDB positron")

for river, coords in rivers_data.items():
    status, color = calculate_imbalance(river)
    
    # Рисуем линию реки
    folium.PolyLine(
        locations=coords, 
        color=color, 
        weight=5, 
        opacity=0.8, 
        tooltip=f"River: {river} | Status: {status}"
    ).add_to(m)
    
    # Добавляем маркер в начале реки с информацией
    folium.Marker(
        location=coords[0], 
        popup=f"<b>{river} River</b><br>Eco Status: {status}",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Добавление легенды
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Экологический статус:</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий дисбаланс<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Умеренный риск<br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Стабильное состояние
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("117.html")

print("Modeling complete. The map has been saved as 117.html")
print("\nAnalysis Summary:")
for river in ["Urzhar", "Aksu"]:
    status, _ = calculate_imbalance(river)
    print(f"River {river}: {status}")