import pandas as pd
import folium

# Загрузка данных (пример: CSV файл)
data = pd.read_csv('water_levels.csv')

# Проверка на наличие пропущенных значений
print(data.isnull().sum())

# Фильтрация данных для неисправных датчиков
unhealthy_sensors = data[data['water_level'].isnull()]

if not unhealthy_sensors.empty:
    print("Неисправные датчики:")
    print(unhealthy_sensors)
else:
    print("Все датчики работают корректно.")

# Создание карты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Добавление маркеров для уровней воды на реках Aksu и Byzhy
for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Река: {row['river']}, Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='blue' if row['river'] == 'Aksu' else 'red')
    ).add_to(m)

# Сохранение карты
m.save("65.html")