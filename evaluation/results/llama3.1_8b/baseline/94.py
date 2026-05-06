import geopandas as gpd
from shapely.geometry import shape
import folium

# Загрузить данные о реках из GeoJSON
gdf_tentek = gpd.read_file('tentek.geojson')
gdf_byzh = gpd.read_file('byzh.geojson')

# Определить начало каждого потока реки (верхнее течение)
def get_upper_stream(gdf):
    # Создать копию геодатафрейма для изменения
    gdf_copy = gdf.copy()
    
    # Добавить новую колонку для хранения верхнего течения
    gdf_copy['upper_stream'] = None
    
    # Произвести топологическую операцию, чтобы найти начало каждого потока реки
    for index, row in gdf_copy.iterrows():
        if row['geometry'].is_ring:
            gdf_copy.loc[index, 'upper_stream'] = shape(row['geometry']).centroid
    
    return gdf_copy

gdf_tentek_upper_stream = get_upper_stream(gdf_tentek)
gdf_byzh_upper_stream = get_upper_stream(gdf_byzh)

# Извлечь координаты начала верхнего течения каждой реки
tentek_coords = (gdf_tentek_upper_stream['upper_stream'].iloc[0].y, gdf_tentek_upper_stream['upper_stream'].iloc[0].x)
byzh_coords = (gdf_byzh_upper_stream['upper_stream'].iloc[0].y, gdf_byzh_upper_stream['upper_stream'].iloc[0].x)

print(f"Координаты верхнего течения реки Тентек: {tentek_coords}")
print(f"Координаты верхнего течения реки Быж: {byzh_coords}")

# Сравнить координаты двух рек
if tentek_coords == byzh_coords:
    print("Координаты верхних течений обоих рек совпадают.")
else:
    print("Координаты верхних течений рек не совпадают.")

# Создать карту с маркерами для каждого верхнего течения
m = folium.Map(location=[gdf_tentek_upper_stream['upper_stream'].iloc[0].y, gdf_tentek_upper_stream['upper_stream'].iloc[0].x], zoom_start=10)
folium.Marker([tentek_coords[0], tentek_coords[1]], popup='Верхнее течение реки Тентек').add_to(m)
folium.Marker([byzh_coords[0], byzh_coords[1]], popup='Верхнее течение реки Быж').add_to(m)

# Сохранить карту в файл
m.save("94.html")