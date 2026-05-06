import geopandas as gpd
import folium
from shapely import wkt

# Загружаем shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создаем карту с центром в середине бассейна и используя плитки CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавляем бассейн на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создаем список словарей с координатами (WKT) для рек Sarykan River и Tekeli River
river_coords = [
    {'name': 'Sarykan River', 'wkt': wkt.loads('POLYGON ((...))')},
    {'name': 'Tekeli River', 'wkt': wkt.loads('POLYGON ((...))')}
]

# Добавляем реки на карту
for river in river_coords:
    folium.GeoJson(
        {
            'type': 'Feature',
            'geometry': river['wkt'].coords,
            'properties': {'name': river['name']}
        },
        name=river['name'],
        style={'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.2}
    ).add_to(m)

# Рассчитываем показатели расхода воды для рек
water_consumption = gdf[gdf['name'].isin([r['name'] for r in river_coords])]

# Добавляем таблицу с показателями расхода воды на карту
folium.Marker(
    location=gdf.centroid.iloc[0],
    popup=folium.Popup(water_consumption.to_html(), max_width=500)
).add_to(m)

# Сохраняем карту в файл
m.save("110.html")