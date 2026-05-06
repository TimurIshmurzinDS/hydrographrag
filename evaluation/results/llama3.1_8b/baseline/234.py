import folium
import pandas as pd

# Сбор данных (предположим, что данные хранятся в DataFrame)
data = {
    'Ресторан': ['Пицца Хаус', 'Дом Пиццы', 'Пиццерия'],
    'Координаты': [(48.8566, 2.3522), (48.8583, 2.2945), (48.8598, 2.3241)],
    'Уровень воды в реке Шарын': [10, 20, 15]
}
df = pd.DataFrame(data)

# Анализ данных
max_water_level = df['Уровень воды в реке Шарын'].max()
min_distance_to_restaurants = df['Координаты'].apply(lambda x: distance_to_point(x, (48.8566, 2.3522))).min()

# Создание модели
model = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

for index, row in df.iterrows():
    if row['Уровень воды в реке Шарын'] > max_water_level * 0.5 and distance_to_point(row['Координаты'], (48.8566, 2.3522)) < min_distance_to_restaurants:
        folium.Marker(location=row['Координаты'], popup=f'Ресторан: {row["Ресторан"]}, Уровень воды в реке Шарын: {row["Уровень воды в реке Шарын"]}').add_to(model)

# Визуализация
m = model
m.save("234.html")