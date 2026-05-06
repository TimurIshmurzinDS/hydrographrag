import folium
import pandas as pd

# 1. Загрузить данные о уровне воды в реке Узын Каргалы.
data = pd.read_csv('uzyn_kargaly_river_data.csv')

# 2. Создать функцию, которая будет рассчитывать уровень жидкости в коктейле на основе данных о уровне воды в реке.
def calculate_drink_level(river_level):
    # Примерная функция для расчета уровня жидкости в коктейле
    drink_level = river_level * 0.5 + 10
    return drink_level

# 3. Визуализировать местоположение реки и уровень жидкости в коктейле на карте с помощью библиотеки Folium.
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for _, row in data.iterrows():
    drink_level = calculate_drink_level(row['river_level'])
    popup_text = f'Уровень реки: {row["river_level"]}\nУровень жидкости в коктейле: {drink_level}'
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=drink_level/10, fill=True).add_to(m)
    folium.Marker([row['latitude'], row['longitude']], popup=popup_text).add_to(m)

# Сохранить карту как HTML-файл
m.save("219.html")