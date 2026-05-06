import pandas as pd
import folium
import matplotlib.pyplot as plt

# Загрузка данных о годовой добыче золота для XIX и XX веков
data_xix = pd.read_csv('gold_production_19th.csv')
data_xx = pd.read_csv('gold_production_20th.csv')

# Преобразование данных в серии временных рядов
ts_xix = pd.Series(data_xix['production'], index=pd.to_datetime(data_xix['year']))
ts_xx = pd.Series(data_xx['production'], index=pd.to_datetime(data_xx['year']))

# Визуализация временных рядов на одной диаграмме
fig, ax = plt.subplots()
ax.plot(ts_xix.index, ts_xix.values, label='XIX век')
ax.plot(ts_xx.index, ts_xx.values, label='XX век')
ax.set_xlabel('Год')
ax.set_ylabel('Добыча золота (тонн)')
ax.legend()
plt.show()

# Создание карты с помощью библиотеки folium
m = folium.Map(location=[0, 0], zoom_start=2)

# Добавление данных о добыче золота на карту в виде точек
for idx, row in data_xix.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=5,
                        color='blue',
                        fill=True,
                        fill_opacity=0.5).add_to(m)

for idx, row in data_xx.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=5,
                        color='red',
                        fill=True,
                        fill_opacity=0.5).add_to(m)

# Сохранение карты в файл HTML
m.save("274.html")