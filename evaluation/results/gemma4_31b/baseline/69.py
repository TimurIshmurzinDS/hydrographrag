import pandas as pd
import folium

# 1. Симуляция данных о датчиках на реках Koktal и Aksu
# В реальном сценарии здесь был бы запрос к API или загрузка CSV/GeoJSON
data = {
    'sensor_id': ['K01', 'K02', 'K03', 'K04', 'A01', 'A02', 'A03', 'A04'],
    'river': ['Koktal River', 'Koktal River', 'Koktal River', 'Koktal River', 
              'Aksu River', 'Aksu River', 'Aksu River', 'Aksu River'],
    'lat': [42.512, 42.530, 42.550, 42.570, 42.610, 42.630, 42.650, 42.670],
    'lon': [77.120, 77.140, 77.160, 77.180, 77.210, 77.230, 77.250, 77.270],
    'status': ['Active', 'Active', 'Inactive', 'Active', 'Active', 'Inactive', 'Inactive', 'Active'],
    'water_level': [1.2, 1.1, 0.0, 1.3, 2.5, 0.0, 0.0, 2.4]
}

df = pd.DataFrame(data)

# 2. Сравнительный анализ статусов
def analyze_sensors(df):
    summary = df.groupby('river')['status'].value_counts().unstack(fill_value=0)
    summary['Total'] = summary.sum(axis=1)
    if 'Active' in summary.columns:
        summary['Health_Rate (%)'] = (summary['Active'] / summary['Total']) * 100
    return summary

analysis_results = analyze_sensors(df)
print("Сравнительный анализ статуса датчиков:")
print(analysis_results)

# 3. Визуализация на карте
# Центрируем карту между двумя реками
m = folium.Map(location=[42.59, 77.20], zoom_start=11, tiles='OpenStreetMap')

# Цветовая схема для статусов
color_map = {'Active': 'green', 'Inactive': 'red'}

# Добавление датчиков на карту
for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"River: {row['river']}<br>ID: {row['sensor_id']}<br>Status: {row['status']}",
        color=color_map[row['status']],
        fill=True,
        fill_color=color_map[row['status']],
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды через HTML-элемент
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Статус датчиков</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block; border-radius:50%"></i> Активен<br>
     <i style="background:red; width:10px; height:10px; display:inline-block; border-radius:50%"></i> Неактивен
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("69.html")

print("\nКарта успешно сохранена в файл 69.html")