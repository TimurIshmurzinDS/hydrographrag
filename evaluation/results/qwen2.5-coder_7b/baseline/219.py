import folium
import numpy as np

# Пример данных о уровне воды в Узун Каргала (в метрах)
water_levels = [10, 12, 15, 13, 14, 16, 17, 18, 19, 20]

# Вычисление среднего и стандартного отклонения
mean_level = np.mean(water_levels)
std_deviation = np.std(water_levels)

# Генерация случайного уровня воды
def generate_water_level(mean, std):
    return np.random.normal(mean, std)

# Генерация рецепта коктейля на основе уровня воды
def generate_drink(water_level):
    if water_level < mean_level - std_deviation:
        return "Коктейль для низкого уровня воды: Водка + Лимонад"
    elif water_level >= mean_level - std_deviation and water_level <= mean_level + std_deviation:
        return "Коктейль для среднего уровня воды: Мартини"
    else:
        return "Коктейль для высокого уровня воды: Красное вино + Шампанское"

# Генерация случайного уровня воды
random_water_level = generate_water_level(mean_level, std_deviation)

# Генерация рецепта коктейля
drink_recipe = generate_drink(random_water_level)
print(f"Случайный уровень воды: {random_water_level:.2f} м")
print(f"Рецепт коктейля: {drink_recipe}")

# Визуализация уровня воды на карте
m = folium.Map(location=[41.3851, 69.2072], zoom_start=13)  # Координаты Узун Каргала

folium.CircleMarker(
    location=[41.3851, 69.2072],
    radius=random_water_level * 10,
    color='blue',
    fill=True,
    fill_color='blue'
).add_to(m)

m.save("219.html")