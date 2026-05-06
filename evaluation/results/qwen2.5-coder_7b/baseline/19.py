import pandas as pd

# Загрузка данных из CSV файла (пример)
data = pd.read_csv('water_levels.csv')

# Предположим, что данные имеют следующие столбцы: 'date', 'water_level'
# Приведение даты к формату datetime
data['date'] = pd.to_datetime(data['date'])

# Фильтрация данных для весеннего паводка (например, с марта по июнь)
spring_start_date = pd.Timestamp(year=data['date'].dt.year, month=3, day=1)
spring_end_date = pd.Timestamp(year=data['date'].dt.year, month=6, day=30)

# Отфильтрованные данные
filtered_data = data[(data['date'] >= spring_start_date) & (data['date'] <= spring_end_date)]

# Определение максимального уровня воды
max_water_level = filtered_data['water_level'].max()

print(f"Максимальный уровень воды, достигнутый во время последнего весеннего паводка на реке Osek River: {max_water_level}")

# Визуализация данных с использованием folium (если требуется)
import folium

# Создание карты
m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=10)

# Добавление маркеров для каждой точки данных
for index, row in filtered_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Уровень воды: {row['water_level']}").add_to(m)

# Сохранение карты в файл
m.save("19.html")