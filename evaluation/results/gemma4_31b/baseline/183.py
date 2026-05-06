import folium
import pandas as pd
import numpy as np

# 1. Имитация данных
# Координаты реки Турген (упрощенно)
river_coords = [
    [42.550, 77.200], [42.560, 77.220], [42.570, 77.250], 
    [42.580, 77.280], [42.590, 77.310], [42.600, 77.350]
]

# Данные о садовых участках
# Area: гектары, Demand_Factor: потребность в м3/га в сутки
orchards_data = {
    'name': ['Сад Северный', 'Сад Центральный', 'Сад Южный', 'Сад Восточный', 'Сад Горный'],
    'lat': [42.555, 42.565, 42.575, 42.585, 42.595],
    'lon': [77.210, 77.230, 77.260, 77.290, 77.330],
    'area': [10, 25, 15, 30, 12], 
    'demand_factor': [50, 50, 60, 50, 70] # м3 на гектар
}

df_orchards = pd.DataFrame(orchards_data)

# Текущее состояние стока реки (м3 в секунду)
# Для примера: низкий сток
current_river_flow = 0.8  # м3/с
seconds_in_day = 86400
total_daily_supply = current_river_flow * seconds_in_day

# 2. Расчет доступности воды
def calculate_status(row, total_supply):
    daily_need = row['area'] * row['demand_factor']
    # Упрощенно: считаем долю потребности от общего стока
    # В реальности учитывается распределение по каналам
    availability_ratio = total_supply / (df_orchards['area'].sum() * 55) # средний норматив
    
    if availability_ratio > 1.2:
        return 'Green', 'Достаточно'
    elif availability_ratio > 0.7:
        return 'Orange', 'Риск дефицита'
    else:
        return 'Red', 'Критический дефицит'

# Применяем расчет
df_orchards[['color', 'status']] = df_orchards.apply(
    lambda row: pd.Series(calculate_status(row, total_daily_supply)), axis=1
)

# 3. Визуализация на карте
m = folium.Map(location=[42.575, 77.275], zoom_start=12, tiles='OpenStreetMap')

# Рисуем реку
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Река Турген").add_to(m)

# Добавляем сады
for idx, row in df_orchards.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        color=row['color'],
        fill=True,
        fill_color=row['color'],
        fill_opacity=0.7,
        popup=f"<b>{row['name']}</b><br>Статус: {row['status']}<br>Площадь: {row['area']} га"
    ).add_to(m)

# Добавляем легенду
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 100px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Доступность воды:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Достаточно<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Риск дефицита<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Критический дефицит
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("183.html")

print("Моделирование завершено. Результаты сохранены в файл 183.html")