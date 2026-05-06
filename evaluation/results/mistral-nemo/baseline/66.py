import geopandas as gpd
import pandas as pd
import folium

# Шаг 1: Сбор данных
data = pd.read_csv('equipment_data.csv')  # Замените 'equipment_data.csv' на путь к вашему файлу данных

# Шаг 2: Подготовка данных
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)
gdf.crs = "EPSG:4326"  # Установите правильную систему координат для ваших данных

# Шаг 3: Геопространственный анализ
working_equipment = gdf[gdf['status'] == 'работает']
non_working_equipment = gdf[gdf['status'] == 'не работает']

# Шаг 4: Визуализация
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

folium.Choropleth(
    gdf,
    name='Оборудование на реке Temirlik River',
    data=gdf,
    columns=['status'],
    key_on='feature.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.8,
    highlight=True
).add_to(m)

folium.LayerControl().add_to(m)

# Шаг 5: Сохранение результатов
m.save("66.html")