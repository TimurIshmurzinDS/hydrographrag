import pandas as pd
import folium

# Загрузим данные о уровнях воды из базы данных или файла
data = pd.read_csv('water_levels.csv')

# Фильтруем данные для получения только рек с повышенным уровнем воды
high_water_rivers = data[data['level'] > 10]  # пример фильтрации: уровень воды выше 10

# Создадим слой на карте, который будет отображать эти реки
m = folium.Map(location=[55.7558, 37.6173], zoom_start=6)

# Добавим информацию об уровне воды к каждой реке
for index, row in high_water_rivers.iterrows():
    river_name = row['name']
    level = row['level']
    folium.Marker([row['lat'], row['lon']], popup=f'{river_name}: {level}').add_to(m)

# Сохраним карту в файл
m.save("high_water_rivers.html")