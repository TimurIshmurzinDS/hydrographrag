import pandas as pd
import geopandas as gpd
from folium import Map, GeoJson


# Загрузка данных о месторождениях и объемах добычи
data = pd.read_csv("gold_mining_data.csv")

# Преобразование данных в GeoDataFrame
geometry = [Point(row["longitude"], row["latitude"]) for index, row in data.iterrows()]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Расчет суммарной добычи по годам
yearly_production = gdf.groupby("year")["production"].sum()

# Создание карты с Folium
m = Map(location=[0, 0], zoom_start=2)

# Добавление точек на карту с цветом в зависимости от объемов добычи
for year in yearly_production.index:
    yearly_data = gdf[gdf["year"] == year]
    geojson = GeoJson(data=yearly_data, name="Production_" + str(year))
    m.add_child(geojson)

# Сохранение карты
m.save("274.html")