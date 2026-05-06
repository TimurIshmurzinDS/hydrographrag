import pandas as pd
import folium

# Шаг 1: Сбор данных о расходе воды для всех постов на реке Temirlik River.
data = pd.read_csv('water_data.csv')  # Предполагается, что данные находятся в CSV-файле

# Шаг 2: Анализ этих данных для определения среднего и пикового расхода воды в каждом из постов.
mean_flow = data.groupby('post_id')['flow'].mean()
peak_flow = data.groupby('post_id')['flow'].max()

# Шаг 3: Определение пороговых значений расхода воды, которые могут привести к наводнению.
threshold = mean_flow * 1.5  # Примерное значение, может быть изменено в зависимости от реальных данных

# Шаг 4: Визуализация этих данных на карте с использованием библиотеки `folium`, чтобы показать вероятность наводнения для каждого поста.
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for _, row in data.iterrows():
    if row['flow'] > threshold:
        color = 'red'
    else:
        color = 'green'

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color=color,
        fill=True
    ).add_to(m)

# Сохранение карты в файл HTML
m.save("78.html")