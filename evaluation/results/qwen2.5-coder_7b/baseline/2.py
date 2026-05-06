import pandas as pd
import folium

# Загрузка данных (пример: CSV файл)
data = pd.read_csv('karatal_water_level_data.csv')

# Предположим, что данные имеют следующие столбцы:
# 'timestamp', 'water_level', 'status'

# Проверка текущего статуса датчика
current_status = data['status'].iloc[-1]
print(f"Текущий статус датчика уровня воды на реке Karatal River: {current_status}")

# Создание карты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Добавление маркера для текущего уровня воды
folium.Marker(
    location=[data['latitude'].iloc[-1], data['longitude'].iloc[-1]],
    popup=f"Текущий уровень воды: {data['water_level'].iloc[-1]}",
    icon=folium.Icon(color='red' if current_status == 'Alert' else 'green')
).add_to(m)

# Сохранение карты как HTML файл
m.save("2.html")