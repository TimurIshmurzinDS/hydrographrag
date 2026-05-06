import geopandas as gpd
import folium

# Загрузка данных о реке Тентек и ее притоках
tentek_river = gpd.read_file("path_to_tentek_river.shp")
tributaries = gpd.read_file("path_to_tributaries.shp")

# Создание карты
m = folium.Map(location=[tentek_river.geometry.centroid.y.mean(), tentek_river.geometry.centroid.x.mean()], zoom_start=10)

# Добавление речной сети на карту
folium.GeoJson(tentek_river, name="Tentek River").add_to(m)
folium.GeoJson(tributaries, name="Tributaries").add_to(m)

# Создание слоя для отображения топологии притоков
def add_tributary_topology(layer):
    for _, row in tributaries.iterrows():
        folium.Marker(
            location=[row.geometry.centroid.y, row.geometry.centroid.x],
            popup=f"Приток: {row['name']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(layer)

# Добавление слоя топологии притоков на карту
tributary_layer = folium.FeatureGroup(name="Tributary Topology")
add_tributary_topology(tributary_layer)
tributary_layer.add_to(m)

# Добавление легенды
folium.LayerControl().add_to(m)

# Сохранение карты
m.save("178.html")

print("Карта сохранена как 178.html")