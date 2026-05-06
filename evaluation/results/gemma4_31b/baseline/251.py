import folium

def generate_kumbel_dessert_map():
    # Координаты примерного расположения реки Кумбель (регион Алтай/Казахстан)
    # Примечание: Для точности используются симулированные точки, 
    # имитирующие структуру речной сети (основной ствол и притоки).
    
    # Центр карты
    center_lat, center_lon = 50.5, 85.0 
    
    # Создание карты
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles='CartoDB positron')

    # 1. Моделирование основного русла (Main Stem) - "Шоколадный ганаш"
    main_river = [
        [50.8, 84.5], [50.7, 84.7], [50.6, 84.8], 
        [50.5, 85.0], [50.4, 85.2], [50.3, 85.4]
    ]
    
    # 2. Моделирование притоков (Tributaries) - "Ягодный сироп"
    tributary_1 = [[50.8, 84.5], [50.9, 84.4], [51.0, 84.6]]
    tributary_2 = [[50.7, 84.7], [50.8, 84.8], [50.8, 84.9]]
    tributary_3 = [[50.5, 85.0], [50.6, 85.1], [50.7, 85.2]]
    tributary_4 = [[50.4, 85.2], [50.3, 85.1], [50.2, 85.0]]

    # Отрисовка основного русла (толстая линия)
    folium.PolyLine(
        main_river, 
        color='darkblue', 
        weight=8, 
        opacity=0.8, 
        tooltip="Основное русло: Шоколадный ганаш"
    ).add_to(m)

    # Отрисовка притоков (тонкие линии)
    tributaries = [tributary_1, tributary_2, tributary_3, tributary_4]
    for i, trib in enumerate(tributaries):
        folium.PolyLine(
            trib, 
            color='skyblue', 
            weight=3, 
            opacity=0.6, 
            tooltip=f"Приток {i+1}: Ягодный сироп"
        ).add_to(m)

    # Добавление маркеров "Кулинарных зон"
    zones = [
        {"loc": [50.8, 84.5], "label": "Начало десерта (Верховья)"},
        {"loc": [50.5, 85.0], "label": "Центральный элемент (Слияние)"},
        {"loc": [50.3, 85.4], "label": "Финишная точка (Устье)"},
    ]

    for zone in zones:
        folium.CircleMarker(
            location=zone["loc"],
            radius=5,
            color='red',
            fill=True,
            fill_color='red',
            popup=zone["label"]
        ).add_to(m)

    # Сохранение карты
    m.save("251.html")
    print("Modeling complete. The 'dessert blueprint' has been saved as 251.html")

if __name__ == "__main__":
    generate_kumbel_dessert_map()