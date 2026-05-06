import pandas as pd
import folium
import random

# 1. Симуляция данных
def generate_sensor_data():
    # Примерные координаты для регионов рек Аягоз и Токыраун (Восточный Казахстан)
    # Примечание: Координаты являются репрезентативными для демонстрации GIS-задачи
    rivers_coords = {
        "Аягоз": {"lat": 49.5, "lon": 79.5},
        "Токыраун": {"lat": 49.2, "lon": 79.1}
    }
    
    sensors = []
    for river, base_coord in rivers_coords.items():
        for i in range(1, 11):  # Создаем по 10 датчиков на каждую реку
            sensor_id = f"SN_{river[:3].upper()}_{i:02d}"
            # Добавляем небольшой случайный сдвиг к координатам, чтобы датчики были распределены вдоль реки
            lat = base_coord["lat"] + random.uniform(-0.2, 0.2)
            lon = base_coord["lon"] + random.uniform(-0.2, 0.2)
            stability = random.uniform(50, 100)  # Стабильность от 50% до 100%
            
            sensors.append({
                "sensor_id": sensor_id,
                "river": river,
                "lat": lat,
                "lon": lon,
                "stability": round(stability, 2)
            })
    
    return pd.DataFrame(sensors)

# 2. Функция определения цвета в зависимости от стабильности
def get_color(stability):
    if stability >= 90:
        return 'green'
    elif stability >= 70:
        return 'orange'
    else:
        return 'red'

# Основной процесс
if __name__ == "__main__":
    # Генерация данных
    df = generate_sensor_data()

    # Расчет общей статистики по рекам
    stats = df.groupby('river')['stability'].mean().reset_index()
    print("--- Отчет о стабильности связи ---")
    for index, row in stats.iterrows():
        print(f"Река {row['river']}: Средняя стабильность = {row['stability']:.2f}%")
    print("----------------------------------\n")

    # 3. Визуализация на карте
    # Центрируем карту в районе исследуемых рек
    m = folium.Map(location=[49.35, 79.3], zoom_start=8, tiles='OpenStreetMap')

    # Добавление датчиков на карту
    for _, row in df.iterrows():
        color = get_color(row['stability'])
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            popup=f"ID: {row['sensor_id']}<br>Река: {row['river']}<br>Стабильность: {row['stability']}%",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)

    # Добавление легенды (простой текстовый элемент в HTML)
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Стабильность связи:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Высокая (>=90%)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средняя (70-89%)<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Низкая (<70%)
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("140.html")
    print("Карта успешно сохранена в файл 140.html")