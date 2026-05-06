import folium
import pandas as pd
import random

# 1. Симуляция данных экологического мониторинга реки Шынжалы
# Координаты подобраны приблизительно для региона реки Шынжалы (Западный Казахстан)
data = {
    'station_id': ['ST_01', 'ST_02', 'ST_03', 'ST_04', 'ST_05'],
    'lat': [51.210, 51.235, 51.260, 51.285, 51.310],
    'lon': [67.120, 67.150, 67.180, 67.210, 67.240],
    'pH': [7.2, 6.8, 5.4, 7.5, 8.1], # Норма: 6.5 - 8.5
    'dissolved_oxygen': [8.5, 7.2, 4.1, 8.0, 7.8], # мг/л (Низкий < 5)
    'nitrates': [12.0, 15.5, 45.0, 10.2, 11.5], # мг/л (Высокий > 40)
    'turbidity': [2.1, 3.5, 8.9, 2.4, 3.0] # NTU
}

df = pd.DataFrame(data)

# 2. Функция для определения цвета маркера на основе экологического состояния
def get_color(row):
    # Критерии: если pH слишком низкий, кислорода мало или нитраты завышены
    if row['pH'] < 6.0 or row['dissolved_oxygen'] < 5.0 or row['nitrates'] > 40:
        return 'red'    # Критическое состояние
    elif row['pH'] < 6.5 or row['nitrates'] > 25:
        return 'orange' # Предупреждение
    else:
        return 'green'  # Норма

# 3. Создание карты
# Центрируем карту на среднем значении координат
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], 
               zoom_start=12, 
               tiles='OpenStreetMap')

# 4. Добавление точек мониторинга на карту
for index, row in df.iterrows():
    color = get_color(row)
    
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>Станция: {row['station_id']}</b><br>"
        f"pH: {row['pH']}<br>"
        f"Кислород (DO): {row['dissolved_oxygen']} мг/л<br>"
        f"Нитраты: {row['nitrates']} мг/л<br>"
        f"Мутность: {row['turbidity']} NTU"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды (простой текстовый элемент)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Статус воды:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Норма<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Предупреждение<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Критический
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# 5. Сохранение карты
m.save("44.html")

print("Modeling complete. The map has been saved as 44.html")