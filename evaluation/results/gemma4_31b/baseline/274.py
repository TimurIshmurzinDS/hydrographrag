import folium
import pandas as pd
import numpy as np

# 1. Подготовка данных
# Создаем репрезентативный набор данных по историческим золотоносным районам
data = {
    'Region': [
        'California (USA)', 'Witwatersrand (South Africa)', 'Klondike (Canada)', 
        'Victoria (Australia)', 'Kolyma (Russia)', 'Carlin Trend (USA)', 
        'West Africa (Ghana/Mali)', 'Central Asia (Kyrgyzstan/Uzbekistan)'
    ],
    'Lat': [38.5, -26.2, 64.0, -36.7, 65.0, 40.7, 7.0, 42.0],
    'Lon': [-120.5, 28.2, -139.0, 144.5, 160.0, -116.2, -2.0, 74.0],
    'Production_19th': [150, 10, 40, 120, 5, 2, 20, 15], # Условные единицы (тыс. тонн)
    'Production_20th': [80, 500, 15, 60, 180, 200, 110, 90]  # Условные единицы (тыс. тонн)
}

df = pd.DataFrame(data)

# 2. Расчет динамики
df['Diff'] = df['Production_20th'] - df['Production_19th']
df['Growth_Ratio'] = df['Production_20th'] / df['Production_19th']
df['Total_Production'] = df['Production_19th'] + df['Production_20th']

# 3. Создание карты
# Центрируем карту так, чтобы были видны основные континенты
m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')

# Функция для определения цвета в зависимости от динамики
def get_color(diff):
    if diff > 0:
        return 'green'  # Рост в XX веке
    else:
        return 'red'    # Спад в XX веке

# 4. Добавление объектов на карту
for index, row in df.iterrows():
    # Определяем размер круга на основе общего объема добычи
    radius = np.sqrt(row['Total_Production']) * 2 
    
    # Создаем всплывающий текст
    popup_text = (
        f"<b>Region:</b> {row['Region']}<br>"
        f"19th Century: {row['Production_19th']} units<br>"
        f"20th Century: {row['Production_20th']} units<br>"
        f"<b>Dynamics:</b> {'Growth' if row['Diff'] > 0 else 'Decline'}<br>"
        f"Difference: {row['Diff']:.2f}"
    )
    
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=radius,
        popup=folium.Popup(popup_text, max_width=300),
        color=get_color(row['Diff']),
        fill=True,
        fill_color=get_color(row['Diff']),
        fill_opacity=0.6,
        weight=2
    ).add_to(m)

# Добавление легенды через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Gold Mining Dynamics</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block;"></i> Growth (20th > 19th)<br>
     <i style="background:red; width:10px; height:10px; display:inline-block;"></i> Decline (20th < 19th)<br>
     <i>Size = Total Volume</i>
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("274.html")

print("Modeling complete. The map has been saved as 274.html")