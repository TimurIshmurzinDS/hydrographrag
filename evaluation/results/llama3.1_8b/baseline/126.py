import pandas as pd
import numpy as np
import folium

# Загрузим данные о стоке рек из исторических записей (предположим, что данные хранятся в файле 'river_flow.csv')
df = pd.read_csv('river_flow.csv')

# Преобразуем данные в формат pandas DataFrame
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Разделим данные на сезонные периоды (весна: март-маю, лето: июнь-август, осень: сентябрь-ноябрь, зима: декабрь-февраль)
seasons = ['spring', 'summer', 'autumn', 'winter']
df['season'] = pd.cut(df.index.month, bins=[1, 3, 6, 9, 12], labels=seasons)

# Оценим среднее значение стока реки для каждого сезонного периода
mean_flow = df.groupby('season')['flow'].mean()

# Сравним средние значения стока реки Шилик с показателями реки Кіші Алматы (предположим, что данные о стоке реки Кіші Алматы хранятся в файле 'kishi_almaty_flow.csv')
kishi_almaty_df = pd.read_csv('kishi_almaty_flow.csv')
kishi_almaty_mean_flow = kishi_almaty_df.groupby('season')['flow'].mean()

# Сравним средние значения стока реки Шилик с показателями реки Кіші Алматы
comparison = mean_flow.to_frame().join(kishi_almaty_mean_flow, lsuffix='_shilik', rsuffix='_kishi_almaty')

# Визуализируем результаты на карте с помощью библиотеки Folium
m = folium.Map(location=[46.5, 78], zoom_start=6)
folium.PolyLine([[46.5, 78], [46.0, 77]], color='red').add_to(m)
folium.Marker([46.5, 78], popup='Река Шилик', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([45.5, 76], popup='Река Кіші Алматы', icon=folium.Icon(color='green')).add_to(m)

# Сохраняем карту в файл
m.save("126.html")