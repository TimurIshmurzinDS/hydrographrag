import folium
import pandas as pd

# Базовый рецепт коктейля (на 1 литр)
basic_recipe = {
    'водка': 0.5,
    'сок лимона': 0.2,
    'сок апельсина': 0.3,
}

# Данные о уровне воды в реке Uzyn Kargaly
water_level_data = pd.DataFrame({
    'location': ['Узун-Каргала'],
    'level': [10, 20, 30]  # на примере трех значений
})

def calculate_liquid(water_level):
    if water_level > 15:
        return basic_recipe['водка'] + 0.1
    elif water_level < 5:
        return basic_recipe['водка'] - 0.2
    else:
        return basic_recipe['водка']

# Создаем карту с маркерами для каждого значения уровня воды
m = folium.Map(location=[43.2333, 79.7333], zoom_start=10)

for i in range(len(water_level_data)):
    folium.Marker(
        location=[water_level_data.loc[i, 'location']],
        popup=f'Уровень воды: {water_level_data.loc[i, "level"]} см',
        icon=folium.Icon(color='blue')
    ).add_to(m)
    
# Добавляем информацию о количестве жидкости для коктейля
for i in range(len(water_level_data)):
    folium.Marker(
        location=[water_level_data.loc[i, 'location']],
        popup=f'Уровень воды: {water_level_data.loc[i, "level"]} см\n'
              f'Количество жидкости для коктейля: {calculate_liquid(water_level_data.loc[i, "level"])} литра',
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохраняем карту в файл
m.save("219.html")