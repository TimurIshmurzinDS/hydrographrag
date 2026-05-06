import pandas as pd
import folium

# Шаг 1: Подготовка данных
data = {
    'river': ['Temirlik River', 'Turgen River'],
    'date': ['2021-01-01', '2021-02-01', ..., '2021-12-01'],  # Заполните данными о расходе воды
    'discharge': [10, 15, ..., 20]  # Заполните данными о расходе воды
}
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Шаг 2: Анализ данных
grouped_data = df.groupby(['river', pd.Grouper(key='date', freq='M')]).mean()
std_dev = grouped_data.groupby('river').std()

# Шаг 3: Визуализация данных
m = folium.Map(location=[43.2, 76.9], zoom_start=8)  # Задайте начальную точку и масштаб карты

for river in ['Temirlik River', 'Turgen River']:
    river_data = grouped_data[grouped_data['river'] == river]
    folium.Choropleth(
        geo_data=river_data,
        columns=['discharge'],
        key_on='feature.properties.river',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.8,
        highlight=True
    ).add_to(m)

# Шаг 4: Оценка риска наводнений (вручную, после визуализации данных)
m.save("83.html")