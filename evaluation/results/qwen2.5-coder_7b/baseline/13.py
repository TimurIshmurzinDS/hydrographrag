import pandas as pd
import folium

# Пример данных (замените на реальные данные)
data = {
    'date': ['2023-10-01', '2023-10-02', '2023-10-03'],
    'river': ['Kumbel River', 'Kumbel River', 'Other River'],
    'water_level': [5.2, 5.4, 6.0]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование даты в формат datetime
df['date'] = pd.to_datetime(df['date'])

# Фильтрация данных для реки Kumbel River
kumbel_data = df[df['river'] == 'Kumbel River']

# Получение последних показаний уровня воды
last_reading = kumbel_data.iloc[-1]

# Создание карты
m = folium.Map(location=[last_reading['water_level'], 0], zoom_start=5)

# Добавление маркера с уровнем воды
folium.Marker(
    location=[last_reading['water_level'], 0],
    popup=f"Последний уровень воды: {last_reading['water_level']} м",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("13.html")