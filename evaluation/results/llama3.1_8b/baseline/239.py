import folium
from folium.plugins import FloatImage

# Загрузите данные о реке Коктал из источника данных (например, GeoJSON или Shapefile)
river_data = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [45.1234, 73.4567],
                    [45.2345, 73.5678],
                    [45.3456, 73.6789]
                ]
            }
        }
    ]
}

# Создайте слой для отображения уровня реки на карте
m = folium.Map(location=[45.2, 73.4], zoom_start=12)

folium.GeoJson(river_data).add_to(m)

# Добавьте функцию для перемещения игрока по карте и проверки расстояния до берега реки
def move_player(player_location):
    player_lat, player_lon = player_location
    river_coords = [(feature['geometry']['coordinates'][0], feature['geometry']['coordinates'][1]) for feature in river_data['features'][0]['geometry']['coordinates']]
    
    # Проверьте расстояние до берега реки
    min_distance = float('inf')
    closest_point = None
    
    for coord in river_coords:
        distance = ((player_lat - coord[0])**2 + (player_lon - coord[1])**2)**0.5
        
        if distance < min_distance:
            min_distance = distance
            closest_point = coord
            
    return closest_point

# Реализуйте логику для победы или поражения в зависимости от того, достиг ли игрок берега реки
def check_win(player_location):
    player_lat, player_lon = player_location
    
    # Если игрок достиг берега реки, выиграл!
    if move_player(player_location) == (player_lat, player_lon):
        return True
    else:
        return False

# Добавьте функцию для перемещения игрока по карте и проверки расстояния до берега реки на карту
def add_player_to_map(m, player_location):
    folium.Marker(player_location, icon=folium.Icon(color='red')).add_to(m)

player_location = [45.2, 73.4]
add_player_to_map(m, player_location)
m.save("239.html")