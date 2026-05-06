import folium
from shapely.geometry import LineString, Point

def generate_borscht_flood_map():
    # 1. Координаты реки Аксу (упрощенная аппроксимация русла для демонстрации)
    # В реальном проекте здесь был бы загружен GeoJSON или Shapefile
    aksu_river_coords = [
        [43.2, 81.5], [43.3, 81.7], [43.4, 81.9], 
        [43.5, 82.1], [43.6, 82.3], [43.7, 82.5]
    ]
    
    # Создаем объект LineString для расчетов
    river_line = LineString(aksu_river_coords)
    
    # 2. Инициализация карты (центр в районе реки Аксу)
    m = folium.Map(location=[43.45, 82.0], zoom_start=8, tiles='CartoDB positron')
    
    # 3. Визуализация "Ингредиентов" (Зон риска)
    
    # Слой "Капуста" (Низкий риск - Зеленый)
    # В folium мы имитируем буфер через круги вдоль линии или широкую линию
    folium.PolyLine(aksu_river_coords, color='green', weight=30, opacity=0.3, 
                    tooltip="Слой 'Капуста': Зона низкого риска (3км)").add_to(m)
    
    # Слой "Картофель" (Средний риск - Желтый)
    folium.PolyLine(aksu_river_coords, color='yellow', weight=15, opacity=0.5, 
                    tooltip="Слой 'Картофель': Зона умеренного риска (1.5км)").add_to(m)
    
    # Слой "Свекла" (Высокий риск - Красный)
    folium.PolyLine(aksu_river_coords, color='red', weight=5, opacity=0.8, 
                    tooltip="Слой 'Свекла': Зона высокого риска (500м)").add_to(m)
    
    # 4. "Зажарка" (Критические точки/Населенные пункты)
    critical_points = [
        {"name": "Поселок А", "coords": [43.32, 81.75], "risk": "Высокий"},
        {"name": "Поселок Б", "coords": [43.51, 82.12], "risk": "Средний"},
        {"name": "Поселок В", "coords": [43.68, 82.45], "risk": "Низкий"},
    ]
    
    for pt in critical_points:
        folium.CircleMarker(
            location=pt["coords"],
            radius=6,
            popup=f"Ингредиент: {pt['name']}<br>Риск: {pt['risk']}",
            color='darkred',
            fill=True,
            fill_color='orange'
        ).add_to(m)

    # 5. Добавление "Рецепта" в виде текстового маркера
    recipe_text = (
        "<b>Рецепт Борща 'Аксу-Риск'</b><br>"
        "1. Бульон: Русло реки Аксу (LineString)<br>"
        "2. Свекла: Красная зона (Buffer 500m)<br>"
        "3. Картофель: Желтая зона (Buffer 1.5km)<br>"
        "4. Капуста: Зеленая зона (Buffer 3km)<br>"
        "5. Зажарка: Точки инфраструктуры<br>"
        "6. Сметана: Финальный рендеринг в .html"
    )
    folium.Marker(
        location=[43.4, 81.4],
        popup=folium.Popup(recipe_text, max_width=300),
        icon=folium.Icon(color='purple', icon='info-sign')
    ).add_to(m)

    # Сохранение результата
    m.save("229.html")
    print("Modeling complete. The 'Borsch' map has been saved as 229.html")

if __name__ == "__main__":
    generate_borscht_flood_map()