import folium
import random

def calculate_apple_pie_recipe(flood_level):
    """
    Функция-трансформер: переводит уровень паводка в ингредиенты пирога.
    """
    # Базовые коэффициенты
    apples = int(flood_level * 2.5)
    flour = int(500 + (flood_level * 15))
    sugar = int(150 + (flood_level * 5))
    baking_time = int(40 + (flood_level * 1.5))
    
    recipe = {
        "apples": apples,
        "flour": flour,
        "sugar": sugar,
        "time": baking_time
    }
    return recipe

def main():
    # 1. Координаты реки Шарын (примерная точка в каньоне)
    sharyn_coords = [43.5000, 79.5000]
    
    # 2. Симуляция уровня паводка (от 0 до 10 метров)
    flood_level = round(random.uniform(0, 10), 2)
    print(f"Текущий уровень паводка реки Шарын: {flood_level} м")
    
    # 3. Расчет рецепта на основе ГИС-параметра
    recipe = calculate_apple_pie_recipe(flood_level)
    
    print("\n--- РЕЦЕПТ ЯБЛОЧНОГО ПИРОГА (ГИДРОЛОГИЧЕСКИЙ МЕТОД) ---")
    print(f"На основе уровня воды {flood_level}м, вам потребуется:")
    print(f"- Яблок: {recipe['apples']} шт.")
    print(f"- Муки: {recipe['flour']} г")
    print(f"- Сахара: {recipe['sugar']} г")
    print(f"- Время выпекания: {recipe['time']} мин")
    print("-------------------------------------------------------\n")

    # 4. Визуализация на карте
    # Создаем карту, центрированную на Шарыне
    m = folium.Map(location=sharyn_coords, zoom_start=10, tiles="OpenStreetMap")

    # Добавляем маркер "Кулинарной станции"
    folium.Marker(
        location=sharyn_coords,
        popup=f"Кухня Шарына\nУровень воды: {flood_level}м\nПирог: {recipe['apples']} яблок",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Визуализируем "зону влияния паводка" (радиус зависит от уровня воды)
    # 1 метр уровня воды = 500 метров радиуса влияния на карте для наглядности
    flood_radius = flood_level * 500 
    folium.Circle(
        location=sharyn_coords,
        radius=flood_radius,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.3,
        popup=f"Зона паводка (Радиус: {flood_radius}м)"
    ).add_to(m)

    # Сохранение карты
    m.save("226.html")
    print("Карта с зоной паводка и точкой приготовления пирога сохранена в файл 226.html")

if __name__ == "__main__":
    main()