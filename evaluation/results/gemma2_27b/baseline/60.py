import geopandas as gpd
import rasterio
from rasterio.plot import show
import folium
import pandas as pd
from scipy.stats import pearsonr

# Загрузка данных осадков и уровня воды
precip_data = rasterio.open("path/to/precipitation_data.tif")
water_level_data = pd.read_csv("path/to/water_level_data.csv", index_col="Date")

# Расчет среднемесячных значений осадков
monthly_precip = precip_data.mean(axis=0)

# Вычисление коэффициентов корреляции
correlations = []
for year in range(2018, 2024):
    yearly_precip = monthly_precip[water_level_data.index.year == year]
    yearly_water_level = water_level_data[water_level_data.index.year == year].values.flatten()
    correlation = pearsonr(yearly_precip, yearly_water_level)[0]
    correlations.append(correlation)

# Создание карты
m = folium.Map(location=[42.8756, 69.2314], zoom_start=8)  # Координаты реки Karkara River

# Добавление слоя осадков на карту
show(monthly_precip, ax=folium.GeoJson(data=gpd.read_file("path/to/karkara_river_basin.shp").to_json(), name="Precipitation"))

# Добавление графиков уровня воды и коэффициентов корреляции
for year, correlation in zip(range(2018, 2024), correlations):
    folium.Marker([42.8756, 69.2314], popup=f"Correlation: {correlation:.2f}").add_to(m)

# Сохранение карты
m.save("60.html")