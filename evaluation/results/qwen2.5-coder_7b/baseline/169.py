import geopandas as gpd
import folium

# Загрузка данных о руселях рек Шынжалы и Талгар
shynjal_rivers = gpd.read_file('path_to_shynjal_rivers.geojson')
talgar_rivers = gpd.read_file('path_to_talgar_rivers.geojson')

# Убедитесь, что данные находятся в одной системе координат (CRS)
if shynjal_rivers.crs != talgar_rivers.crs:
    shynjal_rivers = shynjal_rivers.to_crs(talgar_rivers.crs)

# Определение пересечения
intersection = gpd.overlay(shynjal_rivers, talgar_rivers, how='intersection')

# Визуализация результатов на карте с помощью folium
m = folium.Map(location=[shynjal_rivers.geometry.centroid.y.mean(), shynjal_rivers.geometry.centroid.x.mean()], zoom_start=10)

for _, row in intersection.iterrows():
    if not row.geometry.is_empty:
        folium.GeoJson(row.geometry).add_to(m)

# Сохранение карты
m.save("169.html")