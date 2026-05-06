import folium
import pandas as pd
import numpy as np

# 1. Подготовка синтетических данных о предприятиях на реке Кумбель
# Примечание: Координаты подобраны приблизительно для демонстрации GIS-логики
data = {
    'Enterprise': [
        'Завод "Кумбель-Металл"', 'Агрокомплекс "Степь"', 
        'Текстильный комбинат', 'Пищевой комбинат №1', 
        'Химзавод "Север"', 'Водоканал г. Кумбель'
    ],
    'Lat': [52.1234, 52.1567, 52.1890, 52.2123, 52.2456, 52.2789],
    'Lon': [63.4567, 63.4890, 63.5123, 63.5456, 63.5789, 63.6123],
    'Water_Consumption': [150000, 450000, 80000, 120000, 300000, 500000] # м3 в год
}

df = pd.DataFrame(data)

# 2. Определение координат русла реки (упрощенная линия)
river_coords = [
    [52.1000, 63.4000],
    [52.1234, 63.4567],
    [52.1567, 63.4890],
    [52.1890, 63.5123],
    [52.2123, 63.5456],
    [52.2456, 63.5789],
    [52.2789, 63.6123],
    [52.3000, 63.6500]
]

# 3. Создание карты
# Центрируем карту по средним координатам объектов
m = folium.Map(location=[df['Lat'].mean(), df['Lon'].mean()], zoom_start=11, tiles='OpenStreetMap')

# 4. Визуализация русла реки
folium.PolyLine(
    locations=river_coords, 
    color='blue', 
    weight=5, 
    opacity=0.7, 
    tooltip='Река Кумбель'
).add_to(m)

# 5. Функция для определения цвета в зависимости от объема потребления
def get_color(consumption):
    if consumption > 300000:
        return 'red'    # Высокое потребление
    elif consumption > 100000:
        return 'orange' # Среднее потребление
    else:
        return 'green'  # Низкое потребление

# 6. Добавление предприятий на карту
for index, row in df.iterrows():
    # Масштабирование радиуса круга для визуализации объема (коэффициент 0.05)
    radius = row['Water_Consumption'] * 0.01 
    
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=radius,
        popup=f"<b>{row['Enterprise']}</b><br>Потребление: {row['Water_Consumption']} м³/год",
        color=get_color(row['Water_Consumption']),
        fill=True,
        fill_color=get_color(row['Water_Consumption']),
        fill_opacity=0.6
    ).add_to(m)

# Сохранение результата
m.save("45.html")

print("Моделирование завершено. Карта сохранена в файл 45.html")