import pandas as pd
from folium import Map, Polygon, Marker
from shapely.geometry import shape

# Подготовка данных о реках и их водосборных бассейнах
data = {
    'river': ['Tekeli River', 'Temirlik River'],
    'geometry': [
        {'type': 'Polygon', 'coordinates': [[37.0, 50.0], [38.0, 51.0], [39.0, 52.0], [40.0, 53.0]]},
        {'type': 'Polygon', 'coordinates': [[41.0, 54.0], [42.0, 55.0], [43.0, 56.0], [44.0, 57.0]]}
    ]
}

# Создание геометрий из данных
geometries = []
for river in data['geometry']:
    geometries.append(shape(river))

# Получение данных о потреблении воды для сельского хозяйства
water_consumption_data = pd.DataFrame({
    'river': ['Tekeli River', 'Temirlik River'],
    'consumption': [1000, 2000]
})

# Рассчет суммарного потребления воды
total_water_consumption = water_consumption_data['consumption'].sum()

# Визуализация результатов на карте
m = Map(location=[(geometries[0].bounds.minx + geometries[0].bounds.maxx) / 2, (geometries[0].bounds.miny + geometries[0].bounds.maxy) / 2], zoom_start=10)
for i, geometry in enumerate(geometries):
    polygon = Polygon(location=[[geometry.bounds.minx, geometry.bounds.miny],
                                [geometry.bounds.minx, geometry.bounds.maxy],
                                [geometry.bounds.maxx, geometry.bounds.maxy],
                                [geometry.bounds.maxx, geometry.bounds.miny],
                                [geometry.bounds.minx, geometry.bounds.miny]],
                       color='blue', fill=True)
    m.add_child(polygon)
    marker = Marker(location=[(geometry.bounds.minx + geometry.bounds.maxx) / 2, (geometry.bounds.miny + geometry.bounds.maxy) / 2], popup=f'Река: {data["river"][i]}\nСуммарное потребление воды: {water_consumption_data.loc[i, "consumption"]} м³')
    m.add_child(marker)

# Сохранение карты
m.save("107.html")