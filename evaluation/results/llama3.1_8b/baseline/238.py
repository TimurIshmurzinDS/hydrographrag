import pandas as pd
from pychain import Blockchain
import folium

# Сбор и очистка данных
data = pd.read_csv('osiek_river_flow.csv')
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)

# Обработка данных
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)
mean_flow = data.resample('D').mean()

# Создание блокчейна
blockchain = Blockchain()
for index, row in mean_flow.iterrows():
    blockchain.add_block({
        'timestamp': index,
        'flow': row['flow']
    })

# Визуализация данных на карте
m = folium.Map(location=[50.0, 20.0], zoom_start=10)
folium.Choropleth(
    geo_data='osiek_river.geojson',
    name='choropleth',
    data=data,
    columns=['flow'],
    key_on='feature.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
m.save("238.html")