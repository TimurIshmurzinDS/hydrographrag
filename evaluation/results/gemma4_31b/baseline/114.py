import folium
import pandas as pd

def calculate_irrigation_potential(discharge):
    """
    Рассчитывает суточный объем воды в кубических метрах.
    discharge: расход воды в м3/с
    """
    seconds_in_day = 24 * 60 * 60
    return discharge * seconds_in_day

# 1. Исходные данные (Гипотетические значения для демонстрации моделирования)
# В реальном сценарии данные берутся из API гидрологических служб или CSV-файлов
data = {
    'River': ['Aksu River', 'Kurty River'],
    'Lat': [43.58, 43.82], 
    'Lon': [81.45, 80.65],
    'Current_Discharge': [18.5, 6.2]  # Расход воды в м3/с
}

df = pd.DataFrame(data)

# 2. Расчет потенциала
df['Daily_Volume_m3'] = df['Current_Discharge'].apply(calculate_irrigation_potential)

# Сравнение
aksu_pot = df.loc[df['River'] == 'Aksu River', 'Daily_Volume_m3'].values[0]
kurty_pot = df.loc[df['River'] == 'Kurty River', 'Daily_Volume_m3'].values[0]
ratio = aksu_pot / kurty_pot

print(f"Сравнительный анализ:")
print(f"Потенциал реки Аксу: {aksu_pot:,.2f} м3/сут")
print(f"Потенциал реки Курты: {kurty_pot:,.2f} м3/сут")
print(f"Река Аксу обладает ирригационным потенциалом в {ratio:.2f} раза больше, чем река Курты.")

# 3. Визуализация на карте
# Центрируем карту между двумя реками
m = folium.Map(location=[43.7, 81.0], zoom_start=8, tiles='OpenStreetMap')

# Цвета для маркеров в зависимости от дебита
colors = ['green' if q > 10 else 'orange' for q in df['Current_Discharge']]

for idx, row in df.iterrows():
    popup_text = (
        f"<b>Река:</b> {row['River']}<br>"
        f"<b>Текущий дебит:</b> {row['Current_Discharge']} м3/с<br>"
        f"<b>Суточный объем:</b> {row['Daily_Volume_m3']:,.0f} м3"
    )
    
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=10,
        popup=popup_text,
        color=colors[idx],
        fill=True,
        fill_color=colors[idx],
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда потенциала:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Высокий (>10 м3/с)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний/Низкий (<=10 м3/с)
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("114.html")
print("\nКарта успешно сохранена в файл 114.html")