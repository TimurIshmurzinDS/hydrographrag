import folium
from shapely.geometry import Point, Polygon

# Данные о реке Кумбель и ее сенсорах (примерные данные)
river_data = {
    'type': 'FeatureCollection',
    'features': [
        {
            'geometry': {'type': 'Polygon', 'coordinates': [[
                [48.6784, 44.5223],
                [48.6792, 44.5231],
                [48.6805, 44.5242],
                [48.6818, 44.5253],
                [48.6784, 44.5223]
            ]]},
            'properties': {'name': 'Река Кумбель'}
        },
        {
            'geometry': {'type': 'Point', 'coordinates': [48.6805, 44.5242]},
            'properties': {'status': 'работает', 'id': 1}
        }
    ]
}

# Функция определения статуса сенсора
def get_sensor_status(sensor):
    # Расстояние до ближайшего населенного пункта (примерное значение)
    distance_to_city = 10
    
    if sensor['geometry']['type'] == 'Point':
        point = Point(sensor['geometry']['coordinates'])
        
        # Проверяем, находится ли сенсор внутри реки
        if river_data['features'][0]['geometry']['type'] == 'Polygon' and point.within(river_data['features'][0]['geometry']):
            return sensor['properties']['status']
        else:
            # Если сенсор не внутри реки, то он не работает
            return 'не работает'
    elif sensor['geometry']['type'] == 'LineString':
        # Для линейных геометрий статус определяется отдельно (примерное значение)
        if len(sensor['geometry']['coordinates']) > distance_to_city:
            return 'работает'
        else:
            return 'не работает'

# Создаем карту
m = folium.Map(location=[48.6805, 44.5242], zoom_start=15)

# Добавляем слой сенсоров на карту
for sensor in river_data['features'][1:]:
    status = get_sensor_status(sensor)
    folium.Marker([sensor['geometry']['coordinates'][1], sensor['geometry']['coordinates'][0]], popup=status).add_to(m)

# Сохраняем карту в файл
m.save("6.html")