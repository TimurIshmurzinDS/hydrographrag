import pandas as pd
import folium
from folium import plugins

# Загрузка данных с сенсоров (замените 'data.csv' на фактическое имя файла)
data = pd.read_csv('data.csv')

# Предварительная обработка данных (пример удаления пропусков)
data.dropna(inplace=True)

# Визуализация данных (пример построения графика уровня воды)
data['level'].plot()

# Статистический анализ (пример вычисления среднего значения уровня воды)
average_level = data['level'].mean()
print('Средний уровень воды:', average_level)

# Пространственный анализ (пример создания карты с маркерами сенсоров)
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Сенсор {index}: Уровень воды - {row['level']}"
    ).add_to(m)

# Сохранение карты
m.save("64.html")