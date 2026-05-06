import geopandas as gpd
import folium

# Загрузка данных о сенсорах (предполагается, что данные находятся в shapefile)
sensors = gpd.read_file("sensors_byzhy_river.shp")

# Определение статуса активности сенсоров (пример - из метаданных)
sensors['status'] = sensors['active'].apply(lambda x: 'Активный' if x == 1 else 'Неактивный')

# Создание карты с помощью folium
m = folium.Map(location=[sensors.geometry.y.mean(), sensors.geometry.x.mean()], zoom_start=12)

# Добавление сенсоров на карту с цветовой маркировкой по статусу
for index, row in sensors.iterrows():
    if row['status'] == 'Активный':
        folium.Marker(location=[row.geometry.y, row.geometry.x], 
                      popup=f"Сенсор: {row['name']}<br>Статус: {row['status']}",
                      icon=folium.Icon(color='green')).add_to(m)
    else:
        folium.Marker(location=[row.geometry.y, row.geometry.x], 
                      popup=f"Сенсор: {row['name']}<br>Статус: {row['status']}",
                      icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в HTML-файл
m.save("71.html")