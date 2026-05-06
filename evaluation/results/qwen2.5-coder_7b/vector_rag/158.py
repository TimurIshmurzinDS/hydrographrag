import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках и наблюдениях
bayankol_river = gpd.GeoDataFrame({'geometry': [wkt.loads('LINESTRING(10 20, 30 40)')]})
sarykan_river = gpd.GeoDataFrame({'geometry': [wkt.loads('LINESTRING(50 60, 70 80)')]})

# Загрузка данных о наблюдениях
observations = gpd.GeoDataFrame({
    'geometry': [wkt.loads('POINT(15 25)'), wkt.loads('POINT(35 45)'), wkt.loads('POINT(55 65)')]
})

# Создание карты
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление рек и наблюдений на карту
folium.GeoJson(bayankol_river.to_json()).add_to(m)
folium.GeoJson(sarykan_river.to_json()).add_to(m)
for idx, row in observations.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f"Observation {idx+1}").add_to(m)

# Сохранение карты
m.save("158.html")