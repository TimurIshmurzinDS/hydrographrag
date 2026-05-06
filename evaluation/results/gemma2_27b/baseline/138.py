import pandas as pd
import geopandas as gpd
import folium

# Загрузка данных о уровнях воды из CSV файла
levels = pd.read_csv("water_levels.csv")

# Преобразование данных в GeoDataFrame
gdf = gpd.GeoDataFrame(levels, geometry=gpd.points_from_xy(levels["longitude"], levels["latitude"]))

# Вычисление разницы уровней воды
difference = gdf["Lepsy"] - gdf["Butyk"]

# Создание карты с помощью folium
m = folium.Map(location=[43, 10], zoom_start=8)

# Добавление точек на карту с цветом в зависимости от разницы уровней воды
for index, row in gdf.iterrows():
    folium.CircleMarker(location=(row["geometry"].y, row["geometry"].x), radius=5, color="green" if row["difference"] > 0 else "red").add_to(m)

# Сохранение карты в HTML файл
m.save("138.html")