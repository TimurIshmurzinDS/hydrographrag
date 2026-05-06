import geopandas as gpd
from shapely.geometry import Point
import folium
from scipy.interpolate import griddata

# Загрузка данных о нагрузке наносов
data = gpd.read_file("nanos_data.shp")  # Замените "nanos_data.shp" на имя файла с данными

# Создание списка карт для каждого года
maps = []

# Цикл по годам
for year in range(2019, 2024):
    # Фильтрация данных по году
    year_data = data[data["Year"] == year]

    # Создание сетки для интерполяции
    x = year_data["Longitude"].values
    y = year_data["Latitude"].values
    z = year_data["Concentration"].values
    xi, yi = np.mgrid[-10:10:0.1, -10:10:0.1]  # Определите диапазон координат

    # Интерполяция данных
    zi = griddata((x, y), z, (xi, yi), method='linear')

    # Создание карты
    m = folium.Map(location=[year_data["Latitude"].mean(), year_data["Longitude"].mean()], zoom_start=10)

    # Добавление слоя интерполированных данных
    folium.GeoJson(
        {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[xi[i, j], yi[i, j]] for j in range(len(xi[0]))] for i in range(len(xi))]}},
        style_function=lambda feature: {
            "fillColor": "#ff0000" if zi[int(feature["geometry"]["coordinates"][0][0][1])][int(feature["geometry"]["coordinates"][0][0][0])] > 5 else "#00ff00",
            "fillOpacity": 0.7,
            "color": "black",
            "weight": 1
        }
    ).add_to(m)

    # Добавление точек отбора проб
    for index, row in year_data.iterrows():
        folium.Marker([row["Latitude"], row["Longitude"]], popup=f"Concentration: {row['Concentration']}").add_to(m)

    maps.append(m)

# Сохранение карт
for i, m in enumerate(maps):
    m.save(f"{2019 + i}.html")