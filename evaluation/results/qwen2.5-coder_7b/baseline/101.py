import geopandas as gpd
from shapely.geometry import LineString
import folium

# Загрузка данных о реках (пример данных)
data = {
    'name': ['Емель', 'Тентек', 'Быж'],
    'geometry': [
        LineString([(0, 0), (1, 1)]),
        LineString([(2, 2), (3, 3)]),
        LineString([(4, 4), (5, 5)])
    ]
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry='geometry')

# Функция для определения притоков
def find_sources(gdf):
    sources = []
    for i in range(len(gdf)):
        if i == 0:  # Емель - основная река
            continue
        source_found = False
        for j in range(len(gdf)):
            if j == i:
                continue
            if gdf.geometry[i].intersects(gdf.geometry[j]):
                if gdf.geometry[i].distance(gdf.geometry[j]) < 1e-6:  # Проверка на пересечение
                    sources.append((gdf.name[i], gdf.name[j]))
                    source_found = True
                    break
        if not source_found:
            sources.append((gdf.name[i], None))
    return sources

# Определение притоков
sources = find_sources(gdf)

# Вывод результатов
print("Притоки реки Емель:")
for source in sources:
    if source[1] is not None:
        print(f"{source[0]} является притоком для {source[1]}")

# Визуализация на карте
m = folium.Map(location=[2, 2], zoom_start=5)

folium.GeoJson(gdf.geometry.to_json(), name="Rek").add_to(m)
folium.LayerControl().add_to(m)

for source in sources:
    if source[1] is not None:
        folium.Marker([gdf[gdf['name'] == source[0]].geometry.iloc[0].coords[0]], popup=source[0], icon=folium.Icon(color='red')).add_to(m)
        folium.Marker([gdf[gdf['name'] == source[1]].geometry.iloc[0].coords[0]], popup=source[1], icon=folium.Icon(color='blue')).add_to(m)

m.save("101.html")