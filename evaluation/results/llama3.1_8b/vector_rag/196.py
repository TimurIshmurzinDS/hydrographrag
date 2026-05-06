import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка с данными о расходе воды в Koksu River и Emel River
koksu_data = [
    {'river': 'Koksu', 'value': 100, 'month': 'Январь'},
    {'river': 'Koksu', 'value': 120, 'month': 'Февраль'},
    {'river': 'Koksu', 'value': 110, 'month': 'Март'},
    # Добавьте остальные месяцы аналогично
]

emel_data = [
    {'river': 'Emel', 'value': 90, 'month': 'Январь'},
    {'river': 'Emel', 'value': 130, 'month': 'Февраль'},
    {'river': 'Emel', 'value': 100, 'month': 'Март'},
    # Добавьте остальные месяцы аналогично
]

# Создание визуализации расхода воды в Koksu River и Emel River
folium.Choropleth(
    geo_data=gdf.to_json(),
    name='choropleth',
    data=koksu_data,
    columns=['river', 'value'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

folium.Choropleth(
    geo_data=gdf.to_json(),
    name='choropleth',
    data=emel_data,
    columns=['river', 'value'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

# Сохранение карты в файл
m.save("196.html")