import geopandas as gpd
import folium
from shapely import wkt

def calculate_distance_to_moon():
    # 1. Загрузка данных бассейна (только границы)
    # Используем raw string для пути к файлу
    basin_gdf = gpd.read_file(r"data/basin_data.shp")
    
    # Конвертация в стандартную систему координат WGS84
    basin_gdf = basin_gdf.to_crs('EPSG:4326')
    
    # 2. Инициализация карты
    # Вычисляем центроид бассейна для центрирования карты
    centroid = basin_gdf.geometry.centroid
    center_lat = centroid.y.mean()
    center_lon = centroid.x.mean()
    
    m = folium.Map(
        location=[center_lat, center_lon], 
        tiles='CartoDB positron', 
        zoom_start=10
    )
    
    # Добавление бассейна на карту с заданными параметрами стиля
    folium.GeoJson(
        basin_gdf, 
        style_function=lambda x: {
            'fillColor': 'green', 
            'color': 'darkgreen', 
            'fillOpacity': 0.2
        }
    ).add_to(m)
    
    # 3. Расчет расстояния
    # Поскольку координаты реки и Луны в контексте не предоставлены в WKT,
    # используем константу среднего расстояния от Земли до Луны.
    # В реальной системе здесь был бы запрос к API эфемерид.
    
    avg_distance_km = 384400.0
    entity_river = "Talgar River"
    entity_moon = "Moon"
    
    print(f"Calculating distance between {entity_river} and {entity_moon}...")
    print(f"The average distance is approximately: {avg_distance_km} km")
    
    # 4. Сохранение карты
    m.save("241.html")
    print("Map has been saved as 241.html")

if __name__ == "__main__":
    calculate_distance_to_moon()