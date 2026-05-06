import pandas as pd
import numpy as np
from folium import Map, Marker, CircleMarker
from folium.plugins import HeatMap

# Загрузка данных о уровнях воды в реках (предположим, данные хранятся в файлах csv)
shilik_data = pd.read_csv('shilik_levels.csv')
sharyn_data = pd.read_csv('sharyn_levels.csv')

# Преобразование данных в формат pandas DataFrame
shilik_df = pd.DataFrame(shilik_data)
sharyn_df = pd.DataFrame(sharyn_data)

# Создание временных рядов для каждого года и каждой реки
shilik_ts = shilik_df.groupby('year')['level'].mean().reset_index()
sharyn_ts = sharyn_df.groupby('year')['level'].mean().reset_index()

# Анализ временных рядов для выявления периодов летней засухи (предположим, мы используем метод Moving Average)
shilik_ma = shilik_ts['level'].rolling(window=3).mean()
sharyn_ma = sharyn_ts['level'].rolling(window=3).mean()

# Сравнение результатов анализа для обоих рек
diff_ma = np.abs(shilik_ma - sharyn_ma)

# Создание карты с результатами анализа (используем folium)
m = Map(location=[50.0, 70.0], zoom_start=6)

# Добавление маркеров для каждого года и каждой реки
for i in range(len(shilik_ts)):
    Marker([sharyn_ts['year'].iloc[i], sharyn_ts['level'].iloc[i]]).add_to(m)
    CircleMarker([sharyn_ts['year'].iloc[i], sharyn_ts['level'].iloc[i]], radius=5, color='red').add_to(m)

# Добавление слой с результатами анализа
HeatMap(data=[(x, y, z) for x, y, z in zip(sharyn_ts['year'], sharyn_ts['level'], diff_ma)], radius=10).add_to(m)

# Сохранение карты в файл
m.save("135.html")