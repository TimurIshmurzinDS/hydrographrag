import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (если необходимо)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных стока для Byzhy River и Urzhar River (замените на реальные данные)
data_byzhy = {
    'date': ['2021-01-01', '2021-01-02', '2021-01-03'],
    'flow': [10, 15, 20]
}

data_urzhar = {
    'date': ['2021-01-01', '2021-01-02', '2021-01-03'],
    'flow': [8, 12, 17]
}

# Преобразование данных в DataFrame
df_byzhy = pd.DataFrame(data_byzhy)
df_urzhar = pd.DataFrame(data_urzhar)

# Анализ данных
mean_byzhy = df_byzhy['flow'].mean()
std_byzhy = df_byzhy['flow'].std()

mean_urzhar = df_urzhar['flow'].mean()
std_urzhar = df_urzhar['flow'].std()

print(f"Среднее значение для Byzhy River: {mean_byzhy}, Стандартное отклонение: {std_byzhy}")
print(f"Среднее значение для Urzhar River: {mean_urzhar}, Стандартное отклонение: {std_urzhar}")

# Визуализация данных
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(df_byzhy['date'], df_byzhy['flow'], marker='o', label='Byzhy River')
plt.title('Гидрологический режим Byzhy River')
plt.xlabel('Дата')
plt.ylabel('Поток (м3/с)')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(df_urzhar['date'], df_urzhar['flow'], marker='o', label='Urzhar River')
plt.title('Гидрологический режим Urzhar River')
plt.xlabel('Дата')
plt.ylabel('Поток (м3/с)')
plt.legend()

plt.tight_layout()
plt.show()

# Сохранение карты
m.save("204.html")