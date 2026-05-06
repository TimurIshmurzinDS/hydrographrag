import pandas as pd
import folium

# Загрузка данных
data = {
    'date': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05'],
    'water_level': [1.2, 1.5, 1.8, 2.0, 2.2],
    'historical_average': [1.3, 1.4, 1.5, 1.6, 1.7]
}

df = pd.DataFrame(data)

# Преобразование даты в формат datetime
df['date'] = pd.to_datetime(df['date'])

# Вычисление максимального зафиксированного уровня паводка и его исторического среднего значения
max_water_level = df['water_level'].max()
historical_average = df['historical_average'].mean()

# Рассчитываем разницу
difference = max_water_level - historical_average

print(f"Разница между максимальным зафиксированным уровнем паводка и его историческим средним значением: {difference:.2f}")

# Визуализация данных на карте
m = folium.Map(location=[50.45, 30.52], zoom_start=13)

for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Дата: {row['date']}, Уровень паводка: {row['water_level']:.2f}").add_to(m)

m.save("127.html")