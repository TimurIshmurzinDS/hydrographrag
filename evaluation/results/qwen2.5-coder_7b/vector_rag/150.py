import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках Или и Каратал
il_data = gpd.read_file(r"data/ili_river.shp")
karatal_data = gpd.read_file(r"data/karatal_river.shp")

# Объединение данных о реках в один GeoDataFrame
combined_data = pd.concat([il_data, karatal_data], ignore_index=True)

# Создание карты с использованием центроидов объединенных данных
centroid = combined_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление рек на карту
folium.GeoJson(il_data.to_json(), name="Или", style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)
folium.GeoJson(karatal_data.to_json(), name="Каратал", style_function=lambda x: {'color': 'red', 'weight': 2}).add_to(m)

# Добавление слоя управления для выбора слоев на карте
folium.LayerControl().add_to(m)

# Сохранение карты в файл
m.save("150.html")