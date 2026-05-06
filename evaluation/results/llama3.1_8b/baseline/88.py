import pandas as pd
from folium import Map, Marker

# Сбор данных о постах на реке Koktal River и их текущем уровне воды.
data = {
    'Пост': ['Пост 1', 'Пост 2', 'Пост 3'],
    'Координаты': [[46.4567, 77.1234], [45.6789, 78.9012], [47.8901, 76.5432]],
    'Уровень воды (м)': [10.5, 20.8, 15.3]
}

df = pd.DataFrame(data)

# Создание географической карты с маркерами для каждого поста и информацией об уровне воды.
m = Map(location=[46.7, 77.5], zoom_start=10)
for index, row in df.iterrows():
    marker = Marker(
        location=row['Координаты'],
        popup=f'Пост: {row["Пост"]}<br>Уровень воды: {row["Уровень воды (м)"]} м',
        icon=None
    )
    m.add_child(marker)

# Визуализация карты с помощью библиотеки folium и сохранение ее в файле HTML.
m.save("88.html")