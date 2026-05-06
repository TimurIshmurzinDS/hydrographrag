import geopandas as gpd
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import folium

# Загрузка данных о бассейне реки Уржар
basin = gpd.read_file("data/urzar_basin.shp")

# Загрузка данных о сельскохозяйственных угодьях
agriculture = gpd.read_file("data/agriculture.shp")

# Расчет доступных водных ресурсов (примерная модель)
def calculate_water_resources(elevation, precipitation, evaporation):
    # ... сложная логика расчета с учетом топографии и климата

# Загрузка данных о рельефе и климате
elevation = rasterio.open("data/elevation.tif")
precipitation = rasterio.open("data/precipitation.tif")
evaporation = rasterio.open("data/evaporation.tif")

# Расчет доступных водных ресурсов для каждого участка земли
water_resources = calculate_water_resources(elevation, precipitation, evaporation)

# Определение потребности в воде для сельского хозяйства
agriculture["water_need"] = # ... логика расчета потребности в воде

# Сравнение доступных ресурсов и потребности
deficit = water_resources - agriculture["water_need"]

# Визуализация результатов на карте
m = folium.Map(location=[43.5, 78], zoom_start=10)

# Добавление слоя с бассейном реки Уржар
folium.GeoJson("data/urzar_basin.geojson").add_to(m)

# Добавление слоя с сельскохозяйственными угодьями и раскраска по дефициту воды
for index, row in agriculture.iterrows():
    folium.CircleMarker(location=[row["geometry"].y, row["geometry"].x], radius=50, fill=True, color="red" if row["deficit"] < 0 else "green").add_to(m)

# Сохранение карты
m.save("182.html")