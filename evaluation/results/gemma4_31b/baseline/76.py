import folium
import pandas as pd
import random

def assess_flood_risk(current, critical):
    """
    Оценивает риск паводка на основе текущего и критического расхода воды.
    """
    ratio = current / critical
    if ratio < 0.5:
        return "Низкий", "green"
    elif ratio < 0.8:
        return "Средний", "orange"
    else:
        return "Высокий", "red"

def main():
    # 1. Имитация данных гидропостов на реке Karaoy
    # В реальном сценарии здесь был бы запрос к API или загрузка из GeoJSON/CSV
    data = {
        'station_id': ['KP-01', 'KP-02', 'KP-03', 'KP-04', 'KP-05'],
        'name': ['Верхний Караой', 'Средний Караой-1', 'Средний Караой-2', 'Нижний Караой', 'Устье Караоя'],
        'lat': [42.512, 42.450, 42.380, 42.310, 42.250],
        'lon': [71.120, 71.180, 71.250, 71.320, 71.400],
        'q_current': [12.5, 25.0, 45.2, 68.1, 82.0], # Текущий расход (м3/с)
        'q_critical': [30.0, 40.0, 50.0, 70.0, 90.0] # Критический порог (м3/с)
    }

    df = pd.DataFrame(data)

    # 2. Расчет рисков
    df[['risk_level', 'color']] = df.apply(
        lambda row: pd.Series(assess_flood_risk(row['q_current'], row['q_critical'])), 
        axis=1
    )

    # 3. Создание карты
    # Центрируем карту по средним координатам реки
    center_lat = df['lat'].mean()
    center_lon = df['lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles='OpenStreetMap')

    # Добавление гидропостов на карту
    for index, row in df.iterrows():
        popup_text = (
            f"<b>Пост:</b> {row['name']} ({row['station_id']})<br>"
            f"<b>Текущий расход:</b> {row['q_current']} м³/с<br>"
            f"<b>Крит. порог:</b> {row['q_critical']} м³/с<br>"
            f"<b>Риск паводка:</b> {row['risk_level']}"
        )
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            popup=popup_text,
            color=row['color'],
            fill=True,
            fill_color=row['color'],
            fill_opacity=0.7
        ).add_to(m)

    # Добавление легенды (простой текстовый элемент)
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Уровень риска:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # 4. Сохранение карты
    m.save("76.html")
    print("Анализ завершен. Карта сохранена в файл 76.html")

if __name__ == "__main__":
    main()