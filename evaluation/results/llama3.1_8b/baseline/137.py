import geopandas as gpd
from shapely.geometry import shape
import folium

# Шаг 1: Загрузить данные о местоположении датчиков мониторинга.
датчики = gpd.read_file('датчики.shp')

# Шаг 2: Загрузить данные о границах бассейнов рек Или и Каратал.
бассейны = gpd.read_file('бассейны.shp')

# Создать слой для каждого бассейна
for i, row in бассейны.iterrows():
    name = row['name']
    geometry = shape(row['geometry'])
    
    # Создать слой для текущего бассейна
    layer_name = f'{name}_layer'
    бассейн_геометрия = гpd.GeoDataFrame(geometry=[geometry])
    
    # Объединить данные о местоположении датчиков с данными о границах бассейнов
    joined_data = гpd.sjoin(датчики, бассейн_геометрия, how='inner', op='intersects')
    
    # Определить неисправные датчики как те, которые находятся за пределами своего бассейна
    неисправные_датчики = joined_data[joined_data['geometry'].apply(lambda x: not x.intersects(geometry))]
    
    # Создать слой для текущего бассейна на карте
    map_name = f'{name}_map'
    m = folium.Map(location=[row['y'], row['x']], zoom_start=10)
    folium.GeoJson(неисправные_датчики.to_crs(epsg=3857).geometry.apply(lambda x: {'type': 'Feature', 'geometry': x.__geo_interface__}).tolist()).add_to(m)
    
    # Сохранить карту
    m.save(f'{name}.html')

# Создать общую карту с неисправными датчиками в бассейнах рек Или и Каратал.
м = folium.Map(location=[45.0, 75.0], zoom_start=6)
for i, row in бассейны.iterrows():
    name = row['name']
    geometry = shape(row['geometry'])
    
    # Создать слой для текущего бассейна
    layer_name = f'{name}_layer'
    бассейн_геометрия = гpd.GeoDataFrame(geometry=[geometry])
    
    # Объединить данные о местоположении датчиков с данными о границах бассейнов
    joined_data = гpd.sjoin(датчики, бассейн_геометрия, how='inner', op='intersects')
    
    # Определить неисправные датчики как те, которые находятся за пределами своего бассейна
    неисправные_датчики = joined_data[joined_data['geometry'].apply(lambda x: not x.intersects(geometry))]
    
    # Создать слой для текущего бассейна на карте
    folium.GeoJson(неисправные_датчики.to_crs(epsg=3857).geometry.apply(lambda x: {'type': 'Feature', 'geometry': x.__geo_interface__}).tolist()).add_to(m)

# Сохранить карту
м.save("137.html")