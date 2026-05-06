import geopandas as gpd
import pandas as pd
import folium

# 1. Загрузить данные о местоположении реки Аксу и уровне воды.
data = {
    'name': ['Аксу'],
    'latitude': [43.25],
    'longitude': [76.9],
    'water_level': [10]
}
df = pd.DataFrame(data)

# 2. Создать GeoDataFrame из загруженных данных с помощью geopandas.
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# 3. Вычислить показатели, необходимые для моделирования коктейля
# (например, скорость течения, объем воды).
# Для этого нам понадобится дополнительная информация о рельефе местности,
# ширине реки и других факторах.
# В данном примере мы просто добавим два новых столбца в DataFrame с произвольными значениями.
gdf['flow_speed'] = [5]  # скорость течения
gdf['water_volume'] = [1000000]  # объем воды

# 4. Визуализировать результаты на карте с помощью folium.
m = folium.Map(location=[43.25, 76.9], zoom_start=10)

for index, row in gdf.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

# Сохранить карту в файл "237.html"
m.save("237.html")