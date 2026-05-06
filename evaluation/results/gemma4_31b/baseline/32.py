import folium
import pandas as pd
import numpy as np

# 1. Создание синтетических данных об экологическом состоянии реки Талгар
# Координаты примерно соответствуют течению реки Талгар (от гор к равнине)
data = {
    'station_id': [1, 2, 3, 4, 5],
    'location': ['Верховья (Горы)', 'Среднее течение (Лес)', 'Район г. Талгар', 'Нижнее течение (Поля)', 'Устье/Канал'],
    'lat': [43.1500, 43.1000, 43.0500, 43.0100, 42.9700],
    'lon': [77.5500, 77.6000, 77.6500, 77.7200, 77.8000],
    'wqi': [25, 45, 85, 120, 150],  # Water Quality Index (чем выше, тем хуже)
    'ph': [7.2, 7.4, 7.8, 8.1, 8.5],
    'dissolved_oxygen': [9.5, 8.8, 6.2, 4.5, 3.1] # мг/л
}

df = pd.DataFrame(data)

# Функция для определения цвета в зависимости от индекса WQI
def get_color(wqi):
    if wqi < 50:
        return 'green'
    elif 50 <= wqi < 100:
        return 'orange'
    else:
        return 'red'

# 2. Инициализация карты Folium
# Центрируем карту на среднем течении реки Талгар
m = folium.Map(location=[43.06, 77.67], zoom_start=11, tiles='OpenStreetMap')

# 3. Отрисовка русла реки (упрощенная полилиния)
river_coords = df[['lat', 'lon']].values.tolist()
folium.PolyLine(
    locations=river_coords, 
    color='blue', 
    weight=4, 
    opacity=0.7, 
    tooltip='Русло реки Талгар'
).add_to(m)

# 4. Добавление точек мониторинга на карту
for index, row in df.iterrows():
    status_color = get_color(row['wqi'])
    
    # Формирование текста для всплывающего окна
    popup_text = (
        f"<b>Станция:</b> {row['location']}<br>"
        f"<b>Индекс качества воды (WQI):</b> {row['wqi']}<br>"
        f"<b>pH:</b> {row['ph']}<br>"
        f"<b>Растворенный кислород:</b> {row['dissolved_oxygen']} мг/л<br>"
        f"<b>Статус:</b> {'Чистая' if status_color=='green' else 'Средняя' if status_color=='orange' else 'Загрязненная'}"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        color=status_color,
        fill=True,
        fill_color=status_color,
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=f"Станция {row['station_id']}: {row['location']}"
    ).add_to(m)

# 5. Сохранение итоговой карты
m.save("32.html")

print("Modeling complete. The ecological map of the Talgar River has been saved as '32.html'.")