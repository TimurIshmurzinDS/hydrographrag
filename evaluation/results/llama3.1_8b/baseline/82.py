import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Загрузим данные о постах и реке из соответствующих источников.
posts = pd.read_csv('posts.csv')
river = pd.read_csv('river.csv')

# Создадим географический слой для отображения реки на карте.
m = Map(location=[51.5, 72.0], zoom_start=10)
river_layer = folium.FeatureGroup(name='Река Karaoy River', show=True)
folium.GeoJson(river).add_to(river_layer)

# Создадим еще один географический слой для отображения постов на реке.
posts_layer = folium.FeatureGroup(name='Посты на реке Karaoy River', show=False)
for index, row in posts.iterrows():
    marker = Marker(location=[row['lat'], row['lon']], popup=f'Расход: {row["расход"]}')
    if row['расход'] > 1000: # критическая отметка паводка
        marker.add_to(posts_layer)
posts_layer.add_to(m)

# Добавим слои на карту.
m.add_child(river_layer)
m.add_child(posts_layer)

# Сохраним карту в файл.
m.save("82.html")