import folium

def analyze_river_levels():
    # 1. Исходные данные: координаты, норма и текущий уровень (симуляция данных)
    # Координаты подобраны приблизительно для демонстрации GIS-задачи
    rivers_data = [
        {
            "name": "Baskan River",
            "coords": [45.35, 33.80], 
            "norm_level": 1.2, 
            "current_level": 1.8,  # Превышение
            "unit": "meters"
        },
        {
            "name": "Prokhodnaya River",
            "coords": [45.10, 34.10], 
            "norm_level": 0.8, 
            "current_level": 0.7,  # В норме
            "unit": "meters"
        }
    ]

    # 2. Анализ уровней воды
    exceeding_rivers = []
    normal_rivers = []

    for river in rivers_data:
        if river["current_level"] > river["norm_level"]:
            exceeding_rivers.append(river)
        else:
            normal_rivers.append(river)

    print(f"Реки с превышением уровня: {[r['name'] for r in exceeding_rivers]}")
    print(f"Реки в пределах нормы: {[r['name'] for r in normal_rivers]}")

    # 3. Визуализация на карте
    # Центрируем карту в районе расположения рек
    m = folium.Map(location=[45.22, 33.95], zoom_start=8)

    for river in rivers_data:
        # Определяем цвет маркера в зависимости от уровня воды
        is_exceeding = river["current_level"] > river["norm_level"]
        color = 'red' if is_exceeding else 'green'
        status = "ПРЕВЫШЕНИЕ НОРМЫ" if is_exceeding else "В НОРМЕ"
        
        popup_text = (
            f"<b>Река:</b> {river['name']}<br>"
            f"<b>Статус:</b> {status}<br>"
            f"<b>Текущий уровень:</b> {river['current_level']} {river['unit']}<br>"
            f"<b>Норма:</b> {river['norm_level']} {river['unit']}"
        )

        folium.Marker(
            location=river["coords"],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)

    # Сохранение карты строго в файл 81.html
    m.save("81.html")
    print("Карта успешно сохранена в файл 81.html")

if __name__ == "__main__":
    analyze_river_levels()