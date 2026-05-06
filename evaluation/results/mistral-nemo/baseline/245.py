import geopandas as gpd
from shapely.geometry import LineString
import folium

# 1. Создайте географическую проекцию и загрузите данные о реке Караой в виде линейного объекта.
gdf = gpd.read_file("karakaya_river.shp")  # Замените "karakaya_river.shp" на фактический путь к файлу данных реки Караой

# 2. Вычислите длину реки Караой с помощью функции вычисления длины в геопространстве.
river_length = gdf.iloc[0].geometry.length

# 3. Используйте полученную длину реки для расчета массы черной дыры, используя формулу: масса = длина реки * 10^12
black_hole_mass = river_length * (10 ** 12)

print(f"Масса черной дыры: {black_hole_mass}")

# 4. Визуализируйте реку Караой на карте с помощью библиотеки `folium`, чтобы продемонстрировать географическое расположение реки и результаты расчета.
m = folium.Map(location=[gdf.iloc[0].geometry.y, gdf.iloc[0].geometry.x], zoom_start=12)

# Добавьте реку Караой на карту
folium.GeoJson(gdf.to_json(), name="Караой").add_to(m)

# Сохраните карту как HTML-файл
m.save("245.html")