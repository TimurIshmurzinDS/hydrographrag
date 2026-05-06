import pandas as pd
import folium

# Загрузка данных о расходе воды для обоих годов
data_2020 = pd.read_csv('water_usage_2020.csv')
data_2023 = pd.read_csv('water_usage_2023.csv')

# Объединение данных по месяцам для сравнения
merged_data = pd.merge(data_2020, data_2023, on=['month', 'location'], suffixes=('_2020', '_2023'))

# Создание карты с данными о расходе воды на каждом месяце
m = folium.Map(location=[45.0, 80.0], zoom_start=6)

# Добавление слоев для каждого месяца
for index, row in merged_data.iterrows():
    month = row['month']
    location = row['location']
    usage_2020 = row['usage_2020']
    usage_2023 = row['usage_2023']

    folium.Marker([location[1], location[0]], popup=f'Месяц: {month}, Расход воды в 2020 году: {usage_2020} м³, Расход воды в 2023 году: {usage_2023} м³').add_to(m)

# Визуализация различий в расходе воды между 2020 и 2023 годами
for index, row in merged_data.iterrows():
    month = row['month']
    location = row['location']
    usage_diff = row['usage_2023'] - row['usage_2020']

    if usage_diff > 0:
        color = 'green'
    elif usage_diff < 0:
        color = 'red'
    else:
        color = 'blue'

    folium.CircleMarker([location[1], location[0]], radius=5, color=color).add_to(m)

# Сохранение карты
m.save("58.html")