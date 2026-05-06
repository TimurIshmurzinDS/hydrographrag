import folium
import pandas as pd

def solve_baskan_cooling_problem():
    # 1. Координаты реки Баскан (приблизительный маршрут по Калмыкии)
    # Река протекает в основном с севера на юг/юго-запад
    baskan_coords = [
        [47.2, 44.5], [47.0, 44.8], [46.8, 45.1], 
        [46.5, 45.3], [46.2, 45.5], [45.8, 45.7], 
        [45.5, 45.8], [45.2, 46.0]
    ]

    # 2. Технические параметры воды реки Баскан (моделируемые данные на основе географических фактов)
    water_properties = {
        "Salinity": "Very High (Brackish/Saline)",
        "Flow_Stability": "Intermittent (Seasonal drying)",
        "Corrosiveness": "High",
        "Suitability_Score": "1/10"
    }

    # 3. Создание карты
    # Центрируем карту на среднем значении координат
    m = folium.Map(location=[46.3, 45.2], zoom_start=7, tiles="CartoDB positron")

    # Рисуем линию реки
    folium.PolyLine(
        baskan_coords, 
        color="blue", 
        weight=5, 
        opacity=0.7, 
        tooltip="Река Баскан"
    ).add_to(m)

    # Добавляем маркеры в ключевых точках с анализом
    for i, coord in enumerate(baskan_coords):
        if i % 3 == 0:  # Ставим маркеры не слишком часто
            popup_text = (
                f"<b>Точка анализа {i}</b><br>"
                f"Соленость: {water_properties['Salinity']}<br>"
                f"Стабильность потока: {water_properties['Flow_Stability']}<br>"
                f"Вердикт: Непригодно для охлаждения двигателей."
            )
            folium.CircleMarker(
                location=coord,
                radius=6,
                color="red",
                fill=True,
                fill_color="red",
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(m)

    # Добавляем общую информационную панель (через HTML)
    info_html = f"""
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 300px; height: 160px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px;
                font-family: Arial, sans-serif;">
        <b>Технический отчет ГИС:</b><br>
        Объект: Река Баскан<br>
        Анализ: Высокая минерализация и 
        сезонное пересыхание делают воду 
        непригодной для систем охлаждения 
        космического корабля.<br>
        <b>Риск:</b> Коррозия теплообменников.
    </div>
    """
    m.get_root().html.add_child(folium.Element(info_html))

    # Сохранение карты
    m.save("259.html")
    print("Modeling complete. Map saved as 259.html")

if __name__ == "__main__":
    solve_baskan_cooling_problem()