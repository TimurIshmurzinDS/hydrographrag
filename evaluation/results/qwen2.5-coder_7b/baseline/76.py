import geopandas as gpd
import pandas as pd
import folium

# Загрузка данных о гидропостах и реке Karaoy River
hydrostations = gpd.read_file('hydrostations.shp')
karaoy_river = gpd.read_file('karaoy_river.shp')

# Загрузка данных о текущем расходе воды
water_flow_data = pd.read_csv('water_flow.csv')

# Объединение данных о гидропостах и расходе воды
hydrostations_with_flow = hydrostations.merge(water_flow_data, on='station_id')

# Оценка риска паводка
def calculate_risk(flow_rate):
    if flow_rate > 1000:
        return 'Высокий'
    elif flow_rate > 500:
        return 'Средний'
    else:
        return 'Низкий'

hydrostations_with_flow['risk_level'] = hydrostations_with_flow['flow_rate'].apply(calculate_risk)

# Создание карты
m = folium.Map(location=[karaoy_river.geometry.centroid.y.mean(), karaoy_river.geometry.centroid.x.mean()], zoom_start=10)

# Добавление гидропостов на карту с цветом в зависимости от уровня риска паводка
for idx, row in hydrostations_with_flow.iterrows():
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=5,
        color='red' if row['risk_level'] == 'Высокий' else 
              'orange' if row['risk_level'] == 'Средний' else 
              'green',
        fill=True,
        fill_color='red' if row['risk_level'] == 'Высокий' else 
                         'orange' if row['risk_level'] == 'Средний' else 
                         'green',
        popup=f"Гидропост: {row['station_name']}<br>Риск паводка: {row['risk_level']}",
    ).add_to(m)

# Добавление реки Karaoy River на карту
folium.GeoJson(karaoy_river).add_to(m)

# Сохранение карты
m.save("76.html")