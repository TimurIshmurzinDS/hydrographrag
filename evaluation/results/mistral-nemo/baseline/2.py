import folium
import geopandas as gpd

# Загрузите данные о датчике уровня воды реки Karatal River
river_sensor_data = gpd.read_file("karatal_river_sensor_data.shp")

# Извлеките статус датчика из атрибутов данных
sensor_status = river_sensor_data['status']

# Создайте карту с центром над рекой Karatal River
m = folium.Map(location=[river_sensor_data.geometry.y.mean(), river_sensor_data.geometry.x.mean()], zoom_start=12)

# Добавьте маркеры для каждого датчика уровня воды с их статусами
for idx, row in river_sensor_data.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f"Статус датчика: {sensor_status[idx]}").add_to(m)

# Сохраните карту как HTML-файл
m.save("2.html")