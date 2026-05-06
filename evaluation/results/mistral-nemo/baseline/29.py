import pandas as pd
import folium

# Шаг 1: Получение данных о расходах воды реки Узын-Каргалы во время весеннего паводка.
# Предполагается, что данные находятся в файле 'uzyn_kargaly_water_data.csv'
data = pd.read_csv('uzyn_kargaly_water_data.csv')

# Шаг 2: Анализ и предварительная обработка данных
# Например, заполнение пропущенных значений средним значением по столбцу
data['flow_rate'].fillna(data['flow_rate'].mean(), inplace=True)

# Шаг 3: Визуализация данных на карте с использованием библиотеки `folium`
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['flow_rate']/100,
        color='blue',
        fill=True
    ).add_to(m)

# Шаг 4: Сохранение финальной карты в формате HTML под названием "29.html"
m.save("29.html")