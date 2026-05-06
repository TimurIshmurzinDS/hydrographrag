import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

# 1. Генерация синтетических данных о расходе воды (Гидрограф)
def generate_flood_data(days=30):
    np.random.seed(42)
    dates = [datetime(2024, 3, 1) + timedelta(days=i) for i in range(days)]
    
    # Моделируем паводок: постепенный рост -> пик -> медленный спад
    # Используем функцию Гаусса для имитации пика
    x = np.linspace(-5, 5, days)
    base_flow = 2.0  # Базовый расход м3/с
    peak_flow = 15.0 # Пиковый расход м3/с
    
    # Формула для создания колоколообразной кривой паводка
    discharge = base_flow + peak_flow * np.exp(-x**2 / 2) + np.random.normal(0, 0.5, days)
    
    return pd.DataFrame({'Date': dates, 'Discharge': discharge})

# 2. Подготовка данных
df = generate_flood_data()
max_q = df['Discharge'].max()
peak_date = df.loc[df['Discharge'].idxmax(), 'Date'].strftime('%Y-%m-%d')

# 3. Геоданные реки Batareyka (Примерные координаты для демонстрации)
# В реальном проекте здесь используется GeoJSON или Shapefile
river_coords = [
    [53.450, 32.100], 
    [53.460, 32.120], 
    [53.475, 32.150], 
    [53.490, 32.180], 
    [53.510, 32.210]
]
station_coords = [53.475, 32.150] # Пост наблюдения в середине реки

# 4. Создание интерактивной карты
m = folium.Map(location=station_coords, zoom_start=12, tiles='OpenStreetMap')

# Отрисовка русла реки
folium.PolyLine(
    locations=river_coords, 
    color='blue', 
    weight=5, 
    opacity=0.8, 
    tooltip='Река Batareyka'
).add_to(m)

# Добавление маркера гидрологического поста
popup_text = f"""
    <b>Гидрологический пост Batareyka</b><br>
    Период: Март 2024<br>
    Макс. расход (Qmax): {max_q:.2f} м³/с<br>
    Дата пика: {peak_date}<br>
    Статус: Паводок завершен
"""
folium.CircleMarker(
    location=station_coords,
    radius=8,
    color='red',
    fill=True,
    fill_color='red',
    popup=folium.Popup(popup_text, max_width=300),
    tooltip='Станция мониторинга расхода воды'
).add_to(m)

# Добавление текстовой информации на карту
folium.Popup(f"Анализ паводка: Пик {max_q:.2f} м3/с зафиксирован {peak_date}").add_to(m)

# Сохранение карты
m.save("20.html")

print("Modeling complete. The map has been saved as 20.html")
print(f"Peak discharge: {max_q:.2f} m3/s on {peak_date}")