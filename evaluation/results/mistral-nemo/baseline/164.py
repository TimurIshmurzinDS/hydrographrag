import geopandas as gpd
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from folium import Map, GeoJson, Marker, LayerControl

# 1. Подготовка данных
# Загрузите данные о высоте реки, осадках, температуре воздуха и других факторах в DataFrame
data = pd.read_csv('river_data.csv')

# Загрузите векторные данные рек Или и Шыңжалы в GeoDataFrame
rivers = gpd.read_file('rivers.shp')

# 2. Вычисление риска наводнений
# Определите признаки (features) и целевую переменную (target)
X = data[['river_height', 'precipitation', 'temperature', ...]] # Добавьте другие факторы, влияющие на вероятность паводков
y = data['flood_risk']

# Используйте модель RandomForestClassifier для вычисления риска наводнений
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# 3. Визуализация результатов
# Создайте карту с использованием библиотеки folium
m = Map(location=[43.25, 76.9], zoom_start=8)

# Добавьте векторные данные рек на карту
GeoJson(rivers.to_json(), style_function=lambda x: {'fillColor': 'blue', 'color': 'black'}).add_to(m)

# Вычислите риск наводнений для каждой точки вдоль реки и добавьте маркеры на карту
for _, row in data.iterrows():
    if row['river_name'] == 'Ili River' or row['river_name'] == 'Shynzhaly River':
        risk = clf.predict([row[['river_height', 'precipitation', 'temperature', ...]]]) # Добавьте другие факторы, влияющие на вероятность паводков
        Marker(location=[row['latitude'], row['longitude']], popup=f'Risk: {risk}').add_to(m)

# Добавьте слой контроля для переключения между слоями карты
LayerControl().add_to(m)

# Сохраните карту в формате HTML
m.save("164.html")