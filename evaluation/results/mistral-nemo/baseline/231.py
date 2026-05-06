import geopandas as gpd
import pandas as pd
import folium

# 1. Подготовить данные
data = pd.read_csv('koktal_flood_data.csv') # Замените на путь к вашим данным о половодье реки Коктал
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude'], data['latitude']))

# 2. Проанализировать данные
# Добавить здесь код для анализа данных о половодье реки Коктал

# 3. Моделирование пасты
# Добавить здесь код для моделирования процесса приготовления пасты в зонах затопления реки Коктал

# 4. Визуализация результатов
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

# Сохранить карту как HTML-файл
m.save("231.html")