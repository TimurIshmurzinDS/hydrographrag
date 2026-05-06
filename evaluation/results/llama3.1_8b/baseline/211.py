import folium
import pandas as pd

# Данные о уровне воды в реке Узин Кургалы (предположим, что это CSV-файл)
water_level_data = pd.read_csv('water_level.csv')

# Функция преобразования уровня воды в рецепт пирога
def water_to_recipe(water_level):
    if water_level < 1:
        return 'Вода (1000 грамм)'
    elif water_level <= 2:
        return f'Мука (500 грамм) + Вода ({water_level * 100} грамм)'
    else:
        return f'Масло (200 грамм) + Мука ({(water_level - 2) * 50} грамм) + Вода ({water_level * 20} грамм)'

# Создаем карту
m = folium.Map(location=[43.123, 79.456], zoom_start=10)

# Добавляем данные о уровне воды на карту
for index, row in water_level_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Уровень воды: {row["water_level"]} м\nРецепт пирога: {water_to_recipe(row["water_level"])}').add_to(m)

# Сохраняем карту в HTML-файл
m.save('211.html')