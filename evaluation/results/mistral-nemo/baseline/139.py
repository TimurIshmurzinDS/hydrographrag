import pandas as pd
import folium

# Загрузить данные о реках и датчиках уровня воды
rivers_data = pd.read_csv('rivers.csv')
water_level_data = pd.read_csv('water_levels.csv')

# Отфильтровать данные, чтобы получить только те датчики, которые находятся на реке Сарыкан
sarykan_rivers = rivers_data[rivers_data['river_name'] == 'Сарыкан']
sarykan_water_levels = water_level_data[water_level_data['river_id'].isin(sarykan_rivers['id'])]

# Выявить аномальные показатели уровня воды для каждого датчика
mean_wl = sarykan_water_levels['water_level'].mean()
std_wl = sarykan_water_levels['water_level'].std()
anomalies = sarykan_water_levels[sarykan_water_levels['water_level'] > mean_wl + 2*std_wl]

# Создать карту и отметить реки с аномальными показателями уровня воды
m = folium.Map(location=[51.5074, -0.1278], zoom_start=6)

for _, river in rivers_data.iterrows():
    if river['id'] in anomalies['river_id'].values:
        folium.PolyLine(river['geometry'], weight=3, color='red').add_to(m)
    else:
        folium.PolyLine(river['geometry'], weight=3, color='blue').add_to(m)

# Сохранить карту в файл
m.save("139.html")