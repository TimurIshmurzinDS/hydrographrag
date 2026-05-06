import pandas as pd
import folium

# Пример данных о датчиках (замените на реальные данные)
data = {
    'Датчик': ['Датчик 1', 'Датчик 2', 'Датчик 3'],
    'Широта': [40.7128, 40.7156, 40.7184],
    'Долгота': [-74.0060, -74.0090, -74.0120],
    'Состояние': ['Хорошо', 'Плохо', 'Хорошо'],
    'Время последнего обслуживания': ['2023-01-01', '2022-06-01', '2023-04-01']
}

# Создание DataFrame
df = pd.DataFrame(data)

# Определение необходимости обслуживания (например, если состояние 'Плохо' или время последнего обслуживания более 6 месяцев)
df['Требуется обслуживание'] = df.apply(lambda row: True if row['Состояние'] == 'Плохо' or (pd.to_datetime(row['Время последнего обслуживания']) < pd.Timestamp.now() - pd.DateOffset(months=6)) else False, axis=1)

# Создание карты
m = folium.Map(location=[df['Широта'].mean(), df['Долгота'].mean()], zoom_start=13)

# Добавление маркеров на карте
for index, row in df.iterrows():
    if row['Требуется обслуживание']:
        folium.Marker([row['Широта'], row['Долгота']], popup=f"{row['Датчик']} - Требуется обслуживание", icon=folium.Icon(color='red')).add_to(m)
    else:
        folium.Marker([row['Широта'], row['Долгота']], popup=f"{row['Датчик']} - В порядке", icon=folium.Icon(color='green')).add_to(m)

# Сохранение карты
m.save("146.html")