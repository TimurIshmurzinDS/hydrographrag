import geopandas as gpd
from folium import Map, GeoJson

# Загрузка данных о полях
fields = gpd.read_file("path/to/fields.shp")

# Добавление данных о потреблении воды (пример)
water_needs = {
    "пшеница": 500,  # мм
    "кукуруза": 700, # мм
    "подсолнечник": 400 # мм
}

fields["water_need"] = fields["crop"].map(water_needs)
fields["total_water"] = fields["area"] * fields["water_need"]

# Создание карты
m = Map(location=[52.5, 61.3], zoom_start=8)  # Примерные координаты реки Кумбель

# Добавление слоя полей на карту
GeoJson(fields).add_to(m)

# Сохранение карты
m.save("37.html")