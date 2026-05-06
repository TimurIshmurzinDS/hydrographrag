import rasterio
from rasterstats import zonal_stats
import folium

# Загрузка данных о топографии реки Дос
with rasterio.open("path/to/river_dos_elevation.tif") as src:
    elevation = src.read(1)

# Расчет средней высоты русла
mean_height = elevation.mean()

# Определение остроты соуса на основе высоты
spiciness = int(mean_height / 10)

# Расчет длины русла (предполагаем, что данные о длине уже есть)
river_length = 100 # Заменить на фактическую длину

# Определение густоты соуса на основе длины
thickness = int(river_length / 20)

# Создание рецепта соуса
recipe = f"Рецепт соуса, вкус которого соответствует топографии реки Дос:\n\n"
recipe += f"Острота: {spiciness} единиц остроты (количество перца чили)\n"
recipe += f"Густота: {thickness} единиц густоты (количество муки или крахмала)\n"

# Вывод рецепта
print(recipe)

# Визуализация на карте (необязательно)
m = folium.Map("path/to/river_dos_map.geojson")
m.save("244.html")