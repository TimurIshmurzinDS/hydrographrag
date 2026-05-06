import geopandas as gpd
import folium

# Загрузка данных о бассейнах рек
basin_sarykan = gpd.read_file("sarykan_basin.shp")
basin_emel = gpd.read_file("emel_basin.shp")

# Расчет топологической сложности
nodes_sarykan = len(gpd.GeoSeries(basin_sarykan["geometry"]).to_list()[0].coords)
edges_sarykan = len(basin_sarykan)
total_length_sarykan = sum([len(x) for x in gpd.GeoSeries(basin_sarykan["geometry"]).to_list()])

nodes_emel = len(gpd.GeoSeries(basin_emel["geometry"]).to_list()[0].coords)
edges_emel = len(basin_emel)
total_length_emel = sum([len(x) for x in gpd.GeoSeries(basin_emel["geometry"]).to_list()])

# Вывод результатов
print("Топологическая сложность бассейна реки Сарыкан:")
print(f"Количество узлов: {nodes_sarykan}")
print(f"Количество дуг: {edges_sarykan}")
print(f"Общая длина речной сети: {total_length_sarykan}")

print("\nТопологическая сложность бассейна реки Эмель:")
print(f"Количество узлов: {nodes_emel}")
print(f"Количество дуг: {edges_emel}")
print(f"Общая длина речной сети: {total_length_emel}")

# Визуализация на карте (необязательно)
m = folium.Map()
folium.GeoJson(basin_sarykan).add_to(m)
folium.GeoJson(basin_emel).add_to(m)
m.save("177.html")