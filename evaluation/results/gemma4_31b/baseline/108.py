import folium
import pandas as pd
import numpy as np

# 1. Симуляция данных мониторинга для рек Kurty и Urzhar
# В реальном сценарии здесь будет загрузка из CSV или API гидрологической службы
data = {
    'station_id': ['K1', 'K2', 'K3', 'U1', 'U2', 'U3'],
    'river': ['Kurty', 'Kurty', 'Kurty', 'Urzhar', 'Urzhar', 'Urzhar'],
    'lat': [48.12, 48.25, 48.40, 47.85, 47.98, 48.10],
    'lon': [68.10, 68.22, 68.35, 67.50, 67.65, 67.80],
    'q_avg': [12.5, 10.2, 8.1, 15.0, 12.0, 9.5], # Средний многолетний сток (м3/с)
    'q_current': [11.8, 6.5, 4.2, 14.8, 11.5, 3.1] # Текущий сток (м3/с)
}

df = pd.DataFrame(data)

# 2. Расчет индекса экологического стресса (ESI)
def calculate_stress(row):
    deviation = ((row['q_current'] - row['q_avg']) / row['q_avg']) * 100
    return deviation

df['stress_index'] = df.apply(calculate_stress, axis=1)

# 3. Определение цвета в зависимости от уровня стресса
def get_color(index):
    if abs(index) <= 10:
        return 'green'   # Норма
    elif 10 < abs(index) <= 30:
        return 'orange'  # Умеренный стресс
    else:
        return 'red'     # Высокий стресс

df['color'] = df['stress_index'].apply(get_color)

# 4. Геопространственная визуализация
# Центрирование карты на регионе (примерные координаты Казахстана)
m = folium.Map(location=[48.1, 67.8], zoom_start=8, tiles='CartoDB positron')

# Рисуем линии рек (упрощенно по точкам станций)
rivers = df['river'].unique()
for river_name in rivers:
    river_df = df[df['river'] == river_name]
    coords = river_df[['lat', 'lon']].values.tolist()
    folium.PolyLine(coords, color='blue', weight=3, opacity=0.6, tooltip=f"River {river_name}").add_to(m)

# Добавляем маркеры станций
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        color=row['color'],
        fill=True,
        fill_color=row['color'],
        fill_opacity=0.7,
        popup=(f"Station: {row['station_id']}<br>"
               f"River: {row['river']}<br>"
               f"Current Flow: {row['q_current']} m3/s<br>"
               f"Avg Flow: {row['q_avg']} m3/s<br>"
               f"Stress Index: {row['stress_index']:.2f}%")
    ).add_to(m)

# Добавление легенды
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 110px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Ecological Stress</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Normal (&le;10%)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Moderate (10-30%)<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> High (&gt;30%)
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("108.html")

print("Modeling complete. The map has been saved as 108.html")