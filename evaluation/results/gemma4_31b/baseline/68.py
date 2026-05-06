import folium
import random

def scan_river_sensors():
    # 1. Симуляция данных датчиков на реке Osek River
    # Координаты примерно имитируют течение реки
    river_path = [
        (52.1234, 18.4567), (52.1250, 18.4600), (52.1280, 18.4650),
        (52.1310, 18.4700), (52.1350, 18.4750), (52.1400, 18.4800),
        (52.1450, 18.4850), (52.1500, 18.4900)
    ]
    
    statuses = ["OK", "OK", "OK", "Error", "OK", "Offline", "OK", "OK"]
    sensors_data = []
    
    for i in range(len(river_path)):
        sensors_data.append({
            "id": f"SNSR_{100 + i}",
            "coords": river_path[i],
            "status": statuses[i],
            "value": round(random.uniform(1.2, 3.5), 2) if statuses[i] == "OK" else None
        })

    # 2. Сканирование на предмет неисправностей
    malfunctions = [s for s in sensors_data if s["status"] != "OK"]
    
    print("--- Отчет о сканировании датчиков реки Osek River ---")
    if not malfunctions:
        print("Все датчики работают исправно.")
    else:
        print(f"Обнаружено неисправностей: {len(malfunctions)}")
        for m in malfunctions:
            print(f"Датчик {m['id']}: Статус -> {m['status']} | Координаты: {m['coords']}")
    print("--------------------------------------------------")

    # 3. Визуализация на карте
    # Центрируем карту по средним координатам
    center_lat = sum(s['coords'][0] for s in sensors_data) / len(sensors_data)
    center_lon = sum(s['coords'][1] for s in sensors_data) / len(sensors_data)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='OpenStreetMap')

    # Рисуем линию реки для наглядности
    folium.PolyLine(river_path, color="blue", weight=4, opacity=0.7, tooltip="Osek River").add_to(m)

    # Добавляем маркеры датчиков
    for s in sensors_data:
        color = "green" if s["status"] == "OK" else "red"
        status_text = "Исправен" if s["status"] == "OK" else f"НЕИСПРАВЕН ({s['status']})"
        val_text = f"Уровень: {s['value']}м" if s['value'] else "Данные отсутствуют"
        
        folium.CircleMarker(
            location=s["coords"],
            radius=7,
            popup=f"ID: {s['id']}<br>Статус: {status_text}<br>{val_text}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8
        ).add_to(m)

    # Сохранение карты
    m.save("68.html")
    print("Карта с результатами сканирования сохранена в файл 68.html")

if __name__ == "__main__":
    scan_river_sensors()