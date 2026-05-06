import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
centroid = basin_data.geometry.centroid.iloc[0]
        
# 2. Init map
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 3. Добавляем точки на основе графа знаний
points = [
    {"name": "Река Оск", "wkt": "POINT(20.4567 54.3213)"},
    # К сожалению, в базе данных графа отсутствуют данные о точке максимального уровня воды.
]

# 4. Рисуем маркеры
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("19.html")