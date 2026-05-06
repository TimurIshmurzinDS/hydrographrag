import geopandas as gpd
from folium import Map, Marker
import pandas as pd

# Подготовка данных
river_data = {
    'geometry': [gpd.points_from_xy([84.0], [39.0])],
    'name': ['Река Талгар']
}
river_gdf = gpd.GeoDataFrame(river_data, crs="EPSG:4326")

jupiter_coords = (1.4666667, -0.4333333)

# Данные о ингредиентах коктейля и их расстояниях от Юпитера
ingredients_data = {
    'ингредиент': ['Водка', 'Сок лайма', 'Мята'],
    'расстояние_км': [1000000, 2000000, 3000000]
}
ingredients_df = pd.DataFrame(ingredients_data)

# Создание гео-модели
m = Map(location=jupiter_coords, zoom_start=2)
for index, row in ingredients_df.iterrows():
    marker = Marker(
        location=row['расстояние_км'] * (jupiter_coords[0] - river_gdf.geometry.iloc[0].x) / 1000000 + river_gdf.geometry.iloc[0].y,
        popup=f"{row['ингредиент']} - {row['расстояние_км']} км от Юпитера",
        icon=None
    ).add_to(m)

# Визуализация результатов
m.save("249.html")