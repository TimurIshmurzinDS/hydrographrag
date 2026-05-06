import geopandas as gpd
import folium

# Замените 'path_to_data' на фактический путь к файлу с данными
data = gpd.read_file('path_to_data')

# Создайте карту, центрированную на реке Kumbel
m = folium.Map(location=[latitude, longitude], zoom_start=10) 

# Добавьте слой точек на карту
for index, row in data.iterrows():
    folium.Marker(
        location=[row['geometry'].y, row['geometry'].x],
        popup=f"Уровень воды: {row['water_level']}"  # Замените 'water_level' на название столбца с данными об уровне воды
    ).add_to(m)

# Сохраните карту в HTML-файл
m.save("13.html")