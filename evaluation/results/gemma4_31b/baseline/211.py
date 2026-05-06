import folium
import numpy as np
import random

def get_water_level_color(level):
    """Функция для определения 'вкуса' (цвета) пирога в зависимости от уровня воды"""
    if level < 30:
        return 'orange'  # 'Недопеченный' (низкий уровень)
    elif level < 70:
        return 'green'   # 'Идеально пропеченный' (средний уровень)
    else:
        return 'blue'    # 'Перелился через край' (высокий уровень)

def generate_river_recipe():
    # 1. Координаты реки Узын-Каргалы (приблизительный маршрут для демонстрации)
    # В реальном проекте здесь будет загрузка GeoJSON или Shapefile
    river_coords = [
        [49.21, 67.10], [49.25, 67.20], [49.30, 67.35], 
        [49.35, 67.50], [49.40, 67.65], [49.45, 67.80],
        [49.50, 67.95], [49.55, 68.10]
    ]

    # 2. Генерация 'основного ингредиента' — уровня воды для каждой точки (в см/м)
    # Симулируем данные, так как реальный API гидропостов может быть недоступен
    water_levels = [random.randint(10, 100) for _ in range(len(river_coords))]

    # Создаем карту, центрированную на регионе
    m = folium.Map(location=[49.35, 67.50], zoom_start=8, tiles='CartoDB positron')

    # 3. 'Замешиваем' данные в визуальные элементы
    for i in range(len(river_coords) - 1):
        point_a = river_coords[i]
        point_b = river_coords[i+1]
        level = water_levels[i]
        
        # Рисуем сегмент реки, цвет которого зависит от уровня воды
        folium.PolyLine(
            locations=[point_a, point_b],
            color=get_water_level_color(level),
            weight=6,
            opacity=0.8,
            tooltip=f"Уровень воды: {level} ед."
        ).add_to(m)

    # Добавляем 'украшение' — маркеры в ключевых точках
    for coord, level in zip(river_coords, water_levels):
        folium.CircleMarker(
            location=coord,
            radius=5,
            color='black',
            fill=True,
            fill_color=get_water_level_color(level),
            popup=f"Ингредиент: Уровень воды = {level}"
        ).add_to(m)

    # Добавляем легенду (инструкцию к рецепту)
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;">
     <b>Рецепт Пирога Узын-Каргалы:</b><br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Низкий уровень (Сухой)<br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Средний уровень (Норма)<br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Высокий уровень (Паводок)
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # 4. Сохраняем 'готовое блюдо'
    m.save("211.html")
    print("Модель успешно реализована. 'Пирог' сохранен в файл 211.html")

if __name__ == "__main__":
    generate_river_recipe()