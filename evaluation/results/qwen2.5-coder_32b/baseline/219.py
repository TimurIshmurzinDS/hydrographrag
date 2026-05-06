import requests
import folium

# Шаг 1: Получение данных о уровне воды реки Узун Каргаль
# Предположим, что у нас есть API, который возвращает уровень воды реки
def get_water_level():
    # Пример URL для получения данных (замените на реальный URL)
    url = "https://api.example.com/water-level/uzyn-kargaly"
    response = requests.get(url)
    data = response.json()
    return data['water_level']  # Предположим, что уровень воды возвращается в ключе 'water_level'

# Шаг 2: Обработка данных
def process_water_level(water_level):
    # Преобразуем уровень воды к числовому формату (если необходимо)
    return float(water_level)

# Шаг 3: Определение зависимости уровня жидкости от уровня воды реки
def calculate_cocktail_liquid_level(water_level):
    # Пример линейной зависимости: уровень жидкости коктейля = 0.1 * уровень воды реки + 50 мл
    return 0.1 * water_level + 50

# Шаг 4: Создание рецепта коктейля
def create_cocktail_recipe(liquid_level):
    # Пример рецепта коктейля с учетом уровня жидкости
    recipe = {
        "водка": liquid_level * 0.6,  # 60% водки от общего объема
        "лимонад": liquid_level * 0.3,  # 30% лимонада от общего объема
        "сироп": liquid_level * 0.1    # 10% сиропа от общего объема
    }
    return recipe

# Шаг 5: Визуализация на карте (опционально)
def visualize_on_map(water_level):
    # Координаты реки Узун Каргаль (примерные)
    uzyn_kargaly_coords = [42.8670, 79.1350]
    
    # Создание карты
    m = folium.Map(location=uzyn_kargaly_coords, zoom_start=12)
    
    # Добавление маркера с информацией о уровне воды
    folium.Marker(
        location=uzyn_kargaly_coords,
        popup=f"Уровень воды: {water_level} м",
        icon=folium.Icon(color='blue')
    ).add_to(m)
    
    # Сохранение карты в файл
    m.save("219.html")

# Основной код
if __name__ == "__main__":
    # Получаем уровень воды реки
    water_level = get_water_level()
    
    # Обрабатываем данные
    processed_water_level = process_water_level(water_level)
    
    # Вычисляем уровень жидкости коктейля
    liquid_level = calculate_cocktail_liquid_level(processed_water_level)
    
    # Создаем рецепт коктейля
    cocktail_recipe = create_cocktail_recipe(liquid_level)
    print("Рецепт коктейля:")
    for ingredient, amount in cocktail_recipe.items():
        print(f"{ingredient}: {amount} мл")
    
    # Визуализация на карте
    visualize_on_map(water_level)