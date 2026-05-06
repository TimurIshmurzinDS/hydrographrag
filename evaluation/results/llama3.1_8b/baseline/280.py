import pandas as pd
from folium import Map, Marker
import matplotlib.pyplot as plt

# Шаг 1: Сбор данных
data = {
    'Город': ['Москва', 'Санкт-Петербург', 'Нью-Йорк', 'Лондон'],
    'Год': [2010, 2020, 2015, 2018],
    'Цена жилья': [100000, 150000, 200000, 250000],
    'Цена продуктов': [5000, 6000, 7000, 8000],
    'Цена транспорта': [20000, 30000, 40000, 50000]
}

df = pd.DataFrame(data)

# Шаг 2: Подготовка данных
df['Год'] = pd.to_datetime(df['Год'])
df['Стоимость жизни'] = (df['Цена жилья'] + df['Цена продуктов'] + df['Цена транспорта']) / 3

# Шаг 3: Создание модели
model = df.groupby('Город')['Стоимость жизни'].mean()

# Шаг 4: Анализ данных
print(model)

# Шаг 5: Визуализация результатов
m = Map(location=[55.7558, 37.6173], zoom_start=10)
for index, row in model.iterrows():
    Marker(location=[row.name.latitude, row.name.longitude], popup=f'Стоимость жизни в {index}: {row["Стоимость жизни"]}').add_to(m)

m.save("280.html")