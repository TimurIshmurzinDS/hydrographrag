import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import folium

# Загрузка данных о реках
rivers = gpd.read_file("rivers.shp")

# Загрузка данных о климатических параметрах (например, осадки)
climate_data = rasterio.open("climate_data.tif")

# Расчет зон водосбора для каждой реки
watershed_zones = []
for index, row in rivers.iterrows():
    watershed_zone = gpd.read_file(f"watershed_{row['name']}.shp")
    watershed_zones.append(watershed_zone)

# Расчет уровней водопотребления для каждой реки
water_consumption_levels = []
for i, watershed in enumerate(watershed_zones):
    # Вычисление статистики по зонам водосбора
    stats = zonal_stats(watershed, climate_data, stats="mean")

    # Расчет уровня водопотребления (например, с помощью модели Thornthwaite)
    water_consumption = # ... (вставить код расчета)

    water_consumption_levels.append(water_consumption)

# Создание карты с уровнем водопотребления для каждой реки
m = folium.Map()
for i, river in enumerate(rivers):
    folium.GeoJson(river).add_to(m)
    folium.Marker(location=list(river['geometry'].centroid), popup=f"Уровень водопотребления: {water_consumption_levels[i]}").add_to(m)

# Сохранение карты
m.save("112.html")