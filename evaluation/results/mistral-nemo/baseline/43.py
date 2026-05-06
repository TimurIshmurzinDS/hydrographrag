import geopandas as gpd
from shapely.geometry import Point
import numpy as np

# 1. Получение данных о расходе воды в реке Аягоз.
river_discharge = 50 # м³/с (примерное значение)

# 2. Определение территории, предназначенной для орошения.
# Предполагается, что у нас есть файл с данными о полигонах территории орошения в формате GeoJSON.
орошение_gdf = gpd.read_file("орошение.geojson")

# 3. Расчет пропорции между территорией орошения и общей площадью бассейна реки.
total_area = 1000 # км² (примерное значение площади бассейна реки)
орошение_area = гdf.to_crs("EPSG:4326").geometry.area.sum() / 1e6 # км²
prop = орошение_area / total_area

# 4. Вычисление объема воды, выделяемого на орошение.
орошение_discharge = river_discharge * prop

print(f"Объем воды, выделяемый на орошение в реке Аягоз: {орошение_discharge:.2f} м³/с")

# Визуализация результатов на карте с помощью библиотеки folium (если имеются географические данные).
if не гdf.empty:
    import folium

    # Создание карты.
    m = folium.Map(location=[орошение_gdf.y.mean(), орошение_gdf.x.mean()], zoom_start=10)

    # Добавление полигонов территории орошения на карту.
    орошение_gdf.to_crs("EPSG:4326").plot(column="oro", legend_name="Орошение (м³/с)", ax=m._ax, edgecolor="black")

    # Сохранение карты в файл HTML.
    m.save("43.html")