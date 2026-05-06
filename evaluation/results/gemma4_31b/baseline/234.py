import folium
import random

def generate_sharyn_pizza():
    # 1. Координаты примерного течения реки Шарын (упрощенная линия)
    # В реальности здесь должен быть Shapefile или GeoJSON
    sharyn_river_coords = [
        [43.50, 79.10], [43.55, 79.20], [43.60, 79.35], 
        [43.65, 79.50], [43.70, 79.65], [43.75, 79.80]
    ]

    # Создаем карту, центрированную на регионе Шарына
    m = folium.Map(location=[43.62, 79.45], zoom_start=8, tiles="CartoDB positron")

    # 2. Моделирование "Теста" (Зона сезонного разлива)
    # Мы создаем полигон вокруг реки, имитирующий разлив
    # Для упрощения в folium используем PolyLine и визуальный эффект "широкой линии" 
    # или создаем упрощенный многоугольник (буфер)
    
    # Создаем "основу пиццы" (полигон разлива)
    # Смещаем координаты для создания ширины "теста"
    flood_zone_coords = []
    for lat, lon in sharyn_river_coords:
        flood_zone_coords.append([lat + 0.05, lon + 0.05])
    for lat, lon in reversed(sharyn_river_coords):
        flood_zone_coords.append([lat - 0.05, lon - 0.05])

    folium.Polygon(
        locations=flood_zone_coords,
        color="orange",
        fill=True,
        fill_color="yellow",
        fill_opacity=0.4,
        popup="Основа пиццы (Зона разлива Шарына)"
    ).add_to(m)

    # 3. Добавление "Ингредиентов" (Топпинги)
    # Определяем типы ингредиентов и их цвета
    toppings = {
        "Пепперони (Минералы)": "red",
        "Сыр (Ил и осадки)": "gold",
        "Базилик (Прибрежная флора)": "green",
        "Грибы (Геологические выходы)": "brown"
    }

    # Генерируем случайные точки внутри примерного bounding box зоны разлива
    for topping_name, color in toppings.items():
        for _ in range(10):  # По 10 кусочков каждого ингредиента
            # Генерируем точку в пределах координат реки с небольшим разбросом
            base_point = random.choice(sharyn_river_coords)
            lat = base_point[0] + random.uniform(-0.1, 0.1)
            lon = base_point[1] + random.uniform(-0.1, 0.1)
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                popup=f"Ингредиент: {topping_name}"
            ).add_to(m)

    # 4. Отрисовка самой реки (Центр пиццы)
    folium.PolyLine(
        locations=sharyn_river_coords,
        color="blue",
        weight=3,
        opacity=0.8,
        popup="Русло реки Шарын"
    ).add_to(m)

    # Добавляем заголовок-инструкцию через HTML
    title_html = '''
    <h3 align="center" style="font-size: 16px;"><b>Инструкция по приготовлению ГИС-пиццы "Шарынский разлив"</b></h3>
    <p align="center"><i>Основа: Паводковая зона | Топпинги: Гео-объекты | Запекание: Сезонный цикл</i></p>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    # Сохранение результата
    m.save("234.html")
    print("Modeling complete. Map saved as 234.html")

if __name__ == "__main__":
    generate_sharyn_pizza()