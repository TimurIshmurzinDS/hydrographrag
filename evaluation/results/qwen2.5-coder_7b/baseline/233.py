import geopandas as gpd
import folium

# Загрузка данных о реке Кумбель (пример: Shapefile)
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Создание карты с центром в средних координатах геометрии
center_lat, center_lon = gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Добавление маркера на карте для каждого элемента в GeoDataFrame
for idx, row in gdf.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"Паводок реки Кумбель: {idx}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("233.html")