import geopandas as gpd
from shapely.geometry import shape
import folium

# Загрузим данные о бассейнах рек и их притоках в виде географических объектов (геометрии)
gdf_basin = gpd.read_file('emel_basin.shp')
gdf_sarykan = gpd.read_file('sarykan_river.shp')

# Создадим топологическую связность между бассейнами рек и их притоками
def create_topology(gdf1, gdf2):
    # Сформируем пересечения между геометриями двух данных
    intersection = gpd.overlay(gdf1, gdf2, how='intersection')
    
    # Создадим соединение между геометриями двух данных
    union = gpd.overlay(gdf1, gdf2, how='union')
    
    return intersection, union

# Оценим топологическую связность на основе созданной топологии
def evaluate_topology(intersection, union):
    if not intersection.empty and not union.empty:
        print("Топологическая связность установлена")
    else:
        print("Топологическая связность не установлена")

# Создадим карту с маркерами для каждого бассейна реки и его приток
def create_map(gdf_basin, gdf_sarykan):
    m = folium.Map(location=[50.0, 70.0], zoom_start=6)
    
    for index, row in gdf_basin.iterrows():
        folium.Marker([row.geometry.y, row.geometry.x], popup=row.name).add_to(m)
        
    for index, row in gdf_sarykan.iterrows():
        folium.Marker([row.geometry.y, row.geometry.x], popup=row.name).add_to(m)
    
    m.save("168.html")

# Выполним все шаги
intersection, union = create_topology(gdf_basin, gdf_sarykan)
evaluate_topology(intersection, union)
create_map(gdf_basin, gdf_sarykan)