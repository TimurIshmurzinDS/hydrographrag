import geopandas as gpd
import pandas as pd
import folium

# Шаг 1: Сбор данных
hydro_data = pd.read_csv('sharyn_hydro.csv') # Предполагается, что данные о гидрологическом режиме реки Шарын находятся в файле 'sharyn_hydro.csv'
tourism_data = gpd.read_file('tourism_routes.shp') # Предполагается, что данные о туристических маршрутах находятся в формате Shapefile

# Шаг 2: Анализ данных
hydro_data['change'] = hydro_data['current'] - hydro_data['future'] # Пример расчета изменения гидрологического режима реки Шарын
tourism_data['accessibility'] = tourism_data['length'] * tourism_data['difficulty'] / hydro_data['change'] # Пример расчета доступности туристических маршрутов в зависимости от изменений гидрологического режима реки Шарын

# Шаг 3: Моделирование сценариев
scenario1 = pd.DataFrame({'current': [50, 60, 70], 'future': [40, 50, 60]}) # Пример сценария с уменьшением гидрологического режима реки Шарын на 10%
scenario2 = pd.DataFrame({'current': [50, 60, 70], 'future': [60, 70, 80]}) # Пример сценария с увеличением гидрологического режима реки Шарын на 10%

# Шаг 4: Визуализация результатов
m = folium.Map(location=[53.2798, 71.3486], zoom_start=8) # Координаты и масштаб карты для региона реки Шарын

for index, row in tourism_data.iterrows():
    folium.CircleMarker(
        location=[row['y'], row['x']],
        radius=row['accessibility']/10,
        color='blue',
        fill=True
    ).add_to(m)

m.save("sharyn_tourism.html")