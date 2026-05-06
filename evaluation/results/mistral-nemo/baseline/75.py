import geopandas as gpd
import folium

# Загрузка данных о реках в DataFrame
tentek_river = gpd.read_file('tentek_river.shp')
sharyn_river = gpd.read_file('sharyn_river.shp')

# Сравнение статуса передачи данных между двумя реками
print("Status of data transmission for Tentek River:")
print(tentek_river['data_transmission_status'])

print("\nStatus of data transmission for Sharyn River:")
print(sharyn_river['data_transmission_status'])

# Визуализация результатов на карте
m = folium.Map(location=[50, 80], zoom_start=4)

folium.GeoJson(tentek_river[['geometry']].to_json(), style_function=lambda x: {'fillColor': 'blue', 'color': 'black'}).add_to(m)
folium.GeoJson(sharyn_river[['geometry']].to_json(), style_function=lambda x: {'fillColor': 'red', 'color': 'black'}).add_to(m)

# Сохранение карты в файл
m.save("75.html")