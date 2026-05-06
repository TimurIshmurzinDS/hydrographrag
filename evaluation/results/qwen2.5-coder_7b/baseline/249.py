import folium

# Координаты реки Талгар (пример, реальные координаты могут отличаться)
talgar_coords = [43.0725, 76.9181]  # Широта, Долгота

# Координаты Юпитера в космосе (пример, реальные координаты могут отличаться)
jupiter_coords = [26.6340, -18.3759]  # Широта, Долгота

# Создание карты
m = folium.Map(location=talgar_coords, zoom_start=5)

# Добавление маркера для реки Талгар
folium.Marker(talgar_coords, popup='Река Талгар').add_to(m)

# Добавление маркера для Юпитера
folium.Marker(jupiter_coords, popup='Юпитер').add_to(m)

# Расчет расстояния между точками (примерный расчет)
distance = ((talgar_coords[0] - jupiter_coords[0])**2 + (talgar_coords[1] - jupiter_coords[1])**2)**0.5

# Определение ингредиентов коктейля
if distance < 1000:
    cocktail_ingredients = "Вода и лимон"
else:
    cocktail_ingredients = "Водка и тоник"

# Добавление информации о коктейле на карту
folium.Marker(talgar_coords, popup=f'Река Талгар\nИнгредиенты коктейля: {cocktail_ingredients}').add_to(m)

# Сохранение карты
m.save("249.html")