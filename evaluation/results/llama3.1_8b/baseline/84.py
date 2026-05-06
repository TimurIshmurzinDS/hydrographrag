import pandas as pd
from folium import Map, Marker
import geopandas as gpd

# Шаг 1: Сбор данных о расходе воды и гидропостах
hydro_posts = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Гидропост 1', 'Гидропост 2', 'Гидропост 3'],
    'latitude': [55.1234, 55.4567, 55.7890],
    'longitude': [36.9012, 37.2345, 37.5678]
})

water_flow = pd.DataFrame({
    'date': ['2022-03-01', '2022-03-02', '2022-03-03'],
    'hydro_post_id': [1, 1, 2],
    'water_flow': [100, 120, 150]
})

# Шаг 2: Подготовка данных к анализу
data = pd.merge(water_flow, hydro_posts, on='hydro_post_id')

# Шаг 3: Анализ данных
def find_rapid_increase(data):
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by='date', inplace=True)
    
    for i in range(1, len(data)):
        if (data.iloc[i]['water_flow'] - data.iloc[i-1]['water_flow']) / data.iloc[i-1]['water_flow'] > 0.5:
            return True
    
    return False

rapid_increase = data.groupby('hydro_post_id').apply(find_rapid_increase)

# Шаг 4: Визуализация результатов на карте
m = Map(location=[55.6, 37.2], zoom_start=10)
for index, row in hydro_posts.iterrows():
    if rapid_increase.loc[row['id']]:
        Marker(location=[row['latitude'], row['longitude']], popup=row['name']).add_to(m)

m.save("84.html")