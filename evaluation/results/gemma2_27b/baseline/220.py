import geopandas as gpd
import folium

# Загрузка данных о датчиках Batareyka River (в формате CSV)
sensors = pd.read_csv("sensors_data.csv")

# Создание геопространственной модели реки
river = gpd.read_file("river_shapefile.shp")

# Анализ данных о датчиках

# Определение параметров корабля

# Визуализация

m = folium.Map(location=[river.geometry.y.mean(), river.geometry.x.mean()], zoom_start=12)
folium.GeoJson("river_shapefile.geojson").add_to(m)

# Сохранение карты
m.save("220.html")