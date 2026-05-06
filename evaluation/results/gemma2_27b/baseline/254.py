import geopandas as gpd
import random
import folium

# Загрузка данных о реке
river = gpd.read_file("path/to/river_data.shp")

# Расчет извилистости (замена на реальный расчет)
river["curviness"] = 0  

# Генерация случайных чисел
random_numbers = [random.uniform(0, 1) for _ in range(len(river))]

# Связывание случайных чисел с извилистостью (замена на реальную функцию)
river["random_number"] = random_numbers

# Создание карты Folium
m = folium.Map(location=[river.geometry.y.mean(), river.geometry.x.mean()], zoom_start=12)

# Добавление точек с случайными числами на карту
for index, row in river.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color="blue", fill=True, popup=f"Random Number: {row['random_number']:.2f}").add_to(m)

# Сохранение карты
m.save("254.html")