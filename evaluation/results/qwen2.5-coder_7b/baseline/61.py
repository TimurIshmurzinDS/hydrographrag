import pandas as pd
import folium

# Пример данных: даты, уровни воды и координаты датчиков
data = {
    'date': ['2023-10-01', '2023-10-02', '2023-10-03'],
    'water_level': [5.2, 4.8, 5.0],
    'latitude': [42.123, 42.124, 42.125],
    'longitude': [74.123, 74.124, 74.125]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование даты в datetime
df['date'] = pd.to_datetime(df['date'])

# Установка первой строки как индекс
df.set_index('date', inplace=True)

# Вывод текущего уровня воды
current_water_level = df['water_level'].iloc[-1]
print(f"Текущий уровень воды на реке Aksu River: {current_water_level} м")

# Создание карты
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)

# Добавление маркеров с уровнями воды
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("61.html")