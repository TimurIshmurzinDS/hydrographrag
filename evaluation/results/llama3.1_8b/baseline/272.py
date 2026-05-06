import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Загрузка данных
data = {
    'lat': [43.1234, 43.4567, 43.7890],
    'lon': [69.0123, 69.3456, 69.6789],
    'price_housing': [100000, 120000, 150000],
    'price_goods': [5000, 6000, 7000]
}
df = pd.DataFrame(data)

# Создание карты
m = Map(location=[43.5, 69.3], zoom_start=10)

# Добавление маркеров для каждого региона
for i in range(len(df)):
    Marker(
        location=[df['lat'].iloc[i], df['lon'].iloc[i]],
        popup=f'Регион {i+1}: Цена жилья - {df["price_housing"].iloc[i]}, Цена товаров - {df["price_goods"].iloc[i]}'
    ).add_to(m)

# Создание карты темпов инфляции
heat_data = {
    'lat': df['lat'],
    'lon': df['lon'],
    'value': (df['price_housing'] + df['price_goods']) / 2
}
hm = HeatMap(heat_data, radius=10).add_to(m)

# Сохранение карты в файл
m.save("272.html")