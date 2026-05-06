import folium
import random
from datetime import datetime

def get_koktal_river_depth():
    """
    Симуляция запроса к API гидрологического мониторинга.
    В реальном сценарии здесь был бы запрос к REST API или базе данных SQL.
    """
    # Имитация получения данных с датчика
    # Глубина в метрах
    simulated_depth = round(random.uniform(0.8, 4.5), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return simulated_depth, timestamp

def main():
    # 1. Координаты реки Коктал (примерные координаты для региона)
    # В реальном проекте координаты берутся из Shape-файла или GeoJSON
    river_coords = [42.4500, 72.2100] 
    river_name = "Koktal River"

    # 2. Получение текущих данных о глубине
    depth, time = get_koktal_river_depth()
    
    print(f"Current depth of {river_name}: {depth} meters (Measured at {time})")

    # 3. Создание интерактивной карты
    # Центрируем карту на координатах реки
    m = folium.Map(location=river_coords, zoom_start=13, control_scale=True)

    # Добавление маркера с информацией о глубине
    popup_text = f"<b>River:</b> {river_name}<br><b>Current Depth:</b> {depth} m<br><b>Time:</b> {time}"
    
    folium.Marker(
        location=river_coords,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Click for water depth",
        icon=folium.Icon(color='blue', icon='tint')
    ).add_to(m)

    # Добавление круга влияния (зона мониторинга датчика)
    folium.Circle(
        location=river_coords,
        radius=500, 
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.2,
        popup="Monitoring Zone"
    ).add_to(m)

    # 4. Сохранение карты в файл 11.html
    m.save("11.html")
    print("Map has been saved as 11.html")

if __name__ == "__main__":
    main()