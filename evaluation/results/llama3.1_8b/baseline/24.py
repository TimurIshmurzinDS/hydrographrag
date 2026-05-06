import pandas as pd
import folium

# Подготовка данных
data = {
    'Дата': ['2020-03-01', '2020-04-15', '2021-03-20'],
    'Река': ['Ulken Almaty River', 'Ulken Almaty River', 'Ulken Almaty River'],
    'Высота паводка (м)': [10, 15, 8]
}
df = pd.DataFrame(data)

# Обработка данных
df['Дата'] = pd.to_datetime(df['Дата'])

# Анализ данных
max_height = df.groupby('Река')['Высота паводка (м)'].max().reset_index()
print(max_height)

# Визуализация результатов
m = folium.Map(location=[43.25, 76.95], zoom_start=10)
folium.Marker([43.25, 76.95], popup='Ulken Almaty River').add_to(m)
for index, row in max_height.iterrows():
    folium.CircleMarker(
        location=[row['Река'].split(' ')[1].replace('River', ''), 
                  float(row['Река'].split(' ')[0])],
        radius=row['Высота паводка (м)'],
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)
m.save("24.html")