import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# 3. Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Batareyka River Basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Создание списка наблюдений
observations = [
    {"id": 1, "location": wkt.loads("POINT(55.12345 37.67890)"), "water_level": 10},
    {"id": 2, "location": wkt.loads("POINT(55.23456 37.78901)"), "water_level": 12}
]

# 5. Создание модели прогнозирования
import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.DataFrame({
    'time': [1, 2, 3],
    'water_level': [10, 12, 15]
})

model = LinearRegression()
model.fit(data[['time']], data['water_level'])

# 6. Прогнозирование уровня воды на предстоящий год
future_data = pd.DataFrame({
    'time': [365, 366, 367]
})
predicted_water_levels = model.predict(future_data)

# 7. Вывод прогнозов
for i in range(len(predicted_water_levels)):
    print(f"Прогнозируемый уровень воды на {future_data['time'][i]} день: {predicted_water_levels[i]}")

# 8. Сохранение карты
m.save("55.html")