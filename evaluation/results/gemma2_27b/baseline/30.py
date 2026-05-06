import geopandas as gpd
from rasterio.plot import show
import rasterio
from folium import Map, GeoJson

# 1. Загрузка данных о расходе воды (замените на актуальные данные)
discharge = 100  # м³/с - примерный расход

# 2. Загрузка DEM
dem_path = "path/to/dem.tif"
dem = rasterio.open(dem_path)

# 3. Гидрологическое моделирование (используем упрощенную модель)
# Предполагаем, что зона затопления - это область с высотой ниже уровня воды
water_level = dem.read(1).min() + discharge / 100  # Упрощенная формула

# 4. Расчет индекса риска (используем глубину затопления)
risk_index = water_level - dem.read(1)

# 5. Визуализация результатов
m = Map(location=[56, 38], zoom_start=10)  # Укажите координаты центральной точки

# Создаем GeoJSON из данных риска
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [[...]]},  # Заполните координаты зоны затопления
            "properties": {"risk_index": risk_index.mean()},
        }
    ],
}

GeoJson(geojson_data).add_to(m)
m.save("30.html")