import geopandas as gpd
import pandas as pd
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла GeoJSON: один для бассейнов рек, другой для сельских хозяйств.
basins_gdf = gpd.read_file('path_to_basins.geojson')
farms_gdf = gpd.read_file('path_to_farms.geojson')

# Предположим, что у нас есть CSV файл с данными о потреблении воды каждым хозяйством.
water_consumption_df = pd.read_csv('path_to_water_consumption.csv')

# Шаг 2: Подготовка данных
# Объединение данных о сельских хозяйствах и их потреблении воды
farms_gdf = farms_gdf.merge(water_consumption_df, on='farm_id')

# Шаг 3: Анализ потребления воды
# Вычисление суммарного потребления воды в каждом бассейне реки
basins_gdf['total_water_consumption'] = 0

for index, basin in basins_gdf.iterrows():
    farms_in_basin = farms_gdf[farms_gdf.geometry.within(basin.geometry)]
    total_consumption = farms_in_basin['water_consumption'].sum()
    basins_gdf.at[index, 'total_water_consumption'] = total_consumption

# Шаг 4: Визуализация результатов
# Создание карты с использованием folium
m = folium.Map(location=[basins_gdf.centroid.y.mean(), basins_gdf.centroid.x.mean()], zoom_start=10)

# Добавление бассейнов рек на карту
folium.GeoJson(basins_gdf, name='Бассейны рек').add_to(m)

# Добавление сельских хозяйств на карту с цветовой кодировкой по уровню потребления воды
for _, farm in farms_gdf.iterrows():
    folium.CircleMarker(
        location=[farm.geometry.y, farm.geometry.x],
        radius=5,
        color='blue' if farm['water_consumption'] < 100 else 'red',
        fill=True,
        fill_color='blue' if farm['water_consumption'] < 100 else 'red',
        popup=f"Хозяйство ID: {farm['farm_id']}<br>Потребление воды: {farm['water_consumption']} м³"
    ).add_to(m)

# Добавление легенды
folium.map.LayerControl().add_to(m)

# Сохранение карты в HTML файл
m.save("115.html")