import folium
import math
from datetime import datetime

def calculate_jupiter_distance():
    """
    Аппроксимация расстояния от Земли до Юпитера в миллионах километров.
    Диапазон: ~588 млн км (перигелий) до ~968 млн км (афелий).
    """
    # Используем день года для имитации орбитального цикла
    day_of_year = datetime.now().timetuple().tm_yday
    # Среднее расстояние 778 млн км, амплитуда ~190 млн км
    avg_dist = 778 
    amplitude = 190
    # Синусоидальное изменение в течение года
    distance = avg_dist + amplitude * math.sin(2 * math.pi * day_of_year / 365.25)
    return distance

def generate_cocktail_recipe(distance):
    """
    Генерация рецепта на основе расстояния.
    """
    # 1. Выбор основы (Base)
    if distance < 700:
        base = "Космический Джин (легкость эфира)"
    elif 700 <= distance < 850:
        base = "Галактическая Водка (чистота вакуума)"
    else:
        base = "Межзвездный Темный Ром (глубина космоса)"
    
    # 2. Выбор модификатора (Modifier)
    # Используем остаток от деления для вариативности
    mod_index = int(distance * 100) % 3
    modifiers = {
        0: "Сироп из звездной пыли (черника и лаванда)",
        1: "Нектар Юпитерианских облаков (персик и маракуйя)",
        2: "Экстракт ледяных колец (мята и лайм)"
    }
    modifier = modifiers[mod_index]
    
    # 3. Выбор акцента (Garnish)
    garnish_index = int(distance * 1000) % 2
    garnish = "Щепотка сублимированной малины" if garnish_index == 0 else "Замороженная ягода годжи"
    
    recipe = (
        f"🍹 РЕЦЕПТ: 'Талгарский Юпитерианец'\n"
        f"----------------------------------\n"
        f"1. Основа: {base} (50мл)\n"
        f"2. Модификатор: {modifier} (30мл)\n"
        f"3. Акцент: {garnish}\n"
        f"----------------------------------\n"
        f"Инструкция: Смешать в охлажденном бокале,\n"
        f"всматриваясь в сторону созвездия Стрельца."
    )
    return recipe

def main():
    # Координаты реки Талгар (примерная точка в предгорьях Заилийского Алатау)
    talgar_coords = [43.2167, 77.5167]
    
    # Вычисления
    dist_to_jupiter = calculate_jupiter_distance()
    recipe = generate_cocktail_recipe(dist_to_jupiter)
    
    # Создание карты
    m = folium.Map(location=talgar_coords, zoom_start=10, tiles="CartoDB dark_matter")
    
    # Формирование текста для попапа
    popup_text = (
        f"<b>Точка отсчета: Река Талгар</b><br>"
        f"Расстояние до Юпитера: {dist_to_jupiter:.2f} млн км<br><br>"
        f"{recipe}"
    )
    
    # Добавление маркера
    folium.Marker(
        location=talgar_coords,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Нажми, чтобы узнать рецепт",
        icon=folium.Icon(color="purple", icon="info-sign")
    ).add_to(m)
    
    # Сохранение карты
    m.save("249.html")
    print("Modeling complete. Map saved as 249.html")
    print(f"Current Distance: {dist_to_jupiter:.2f} million km")
    print(recipe)

if __name__ == "__main__":
    main()