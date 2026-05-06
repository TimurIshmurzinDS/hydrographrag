import folium
import pandas as pd
import numpy as np

# 1. Подготовка данных
# Создаем словарь с координатами городов и имитацией стоимости жизни (индексные значения)
# Стоимость 1924 года приведена к условным единицам для сравнения трендов
data = {
    'City': ['New York', 'London', 'Tokyo', 'Paris', 'Moscow', 'Hong Kong', 'Berlin', 'Sydney'],
    'Lat': [40.7128, 51.5074, 35.6895, 48.8566, 55.7558, 22.3193, 52.5200, -33.8688],
    'Lon': [-74.0060, -0.1278, 139.6917, 2.3522, 37.6173, 114.1694, 13.4050, 151.2093],
    'Cost_1924': [100, 90, 40, 85, 50, 30, 70, 60], # Условные единицы
    'Cost_2024': [1200, 1100, 950, 1050, 800, 1300, 850, 900] # Условные единицы
}

df = pd.DataFrame(data)

# 2. Расчет показателей
# Вычисляем процент роста стоимости проживания за 100 лет
df['Growth_Rate'] = ((df['Cost_2024'] - df['Cost_1924']) / df['Cost_1924']) * 100

# Функция для определения цвета в зависимости от темпа роста
def get_color(growth):
    if growth > 3000:
        return 'red'    # Экстремальный рост
    elif growth > 1000:
        return 'orange' # Высокий рост
    else:
        return 'green'  # Умеренный рост

# 3. Создание карты
# Центрируем карту (среднее значение координат)
m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

# Добавление маркеров на карту
for index, row in df.iterrows():
    # Определяем размер круга на основе текущей стоимости (масштабирование для визуализации)
    radius = row['Cost_2024'] / 20 
    
    # Создаем текст для всплывающего окна
    popup_text = (
        f"<b>City:</b> {row['City']}<br>"
        f"Cost 1924: {row['Cost_1924']} units<br>"
        f"Cost 2024: {row['Cost_2024']} units<br>"
        f"<b>Growth: {row['Growth_Rate']:.2f}%</b>"
    )
    
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=radius,
        popup=folium.Popup(popup_text, max_width=300),
        color=get_color(row['Growth_Rate']),
        fill=True,
        fill_color=get_color(row['Growth_Rate']),
        fill_opacity=0.6,
        weight=2
    ).add_to(m)

# Добавление легенды (простой текстовый элемент в HTML)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 100px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Growth Intensity:</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Extreme (>3000%)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> High (>1000%)<br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Moderate
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# 4. Сохранение результата
m.save("280.html")

print("Modeling complete. The map has been saved as 280.html")