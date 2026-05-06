import geopandas as gpd
from rasterio import open as rio_open
from rasterio.plot import show
import folium
from shapely.geometry import Point

# Загрузка данных
river = gpd.read_file("river_karakara.shp")
pollution_sources = gpd.read_file("pollution_sources.shp")
elevation = rio_open("elevation.tif")
soil = rio_open("soil.tif")
vegetation = rio_open("vegetation.tif")

# Предобработка данных (пример)
pollution_sources['buffer'] = pollution_sources['intensity'].apply(lambda x: x * 100) # Пример буферизации
pollution_sources['geometry'] = pollution_sources['geometry'].buffer(pollution_sources['buffer'])

# Оценка риска (примерная модель)
def risk_assessment(x, y):
    distance_to_source = min([p.distance(Point(x, y)) for p in pollution_sources['geometry']])
    elevation_value = elevation.read(1, window=((y, y+1), (x, x+1)))[0][0]
    soil_type = soil.read(1, window=((y, y+1), (x, x+1)))[0][0]
    vegetation_type = vegetation.read(1, window=((y, y+1), (x, x+1)))[0][0]

    # Логика расчета риска на основе факторов
    risk = distance_to_source * elevation_value / soil_type * vegetation_type 
    return risk

# Создание растровой модели риска
risk_raster = rio_open("risk.tif", 'w', driver='GTiff', width=elevation.width, height=elevation.height, count=1, dtype=float)
for y in range(elevation.height):
    for x in range(elevation.width):
        risk = risk_assessment(x, y)
        risk_raster.write(risk, 1, window=((y, y+1), (x, x+1)))

# Визуализация на карте
m = folium.Map(location=[river.geometry.centroid.y, river.geometry.centroid.x], zoom_start=10)
folium.GeoJson(river).add_to(m)
folium.GeoJson(pollution_sources).add_to(m)

# Добавление растровой модели риска на карту (пример)
risk_layer = folium.raster_layers.ImageOverlay("risk.tif", opacity=0.7, mercator_projection=True)
risk_layer.add_to(m)

m.save("38.html")