import folium
from astroquery.horizons import Horizons

# Вычисление расстояния
h = Horizons(id='Jupiter', location=True)
distance_data = h.ephemerides(epochs=['2023-10-27'])
distance_km = distance_data['r'][0] * 149597870.7

# Категоризация расстояния
if distance_km <= 100e6:
    ingredients = "Vodka, Orange Juice, Lemon Syrup"
elif distance_km <= 200e6:
    ingredients = "Gin, Tonic, Lime"
else:
    ingredients = "Rum, Cola, Mint"

# Создание карты
m = folium.Map(location=[43.1589, 77.0286], zoom_start=5)
folium.Marker([43.1589, 77.0286], popup="Talgar River", icon=folium.Icon(color='blue')).add_to(m)

# Маркер Юпитера (координаты примерные)
folium.Marker([0, 0], popup="Jupiter", icon=folium.Icon(color='red')).add_to(m)

# Добавление текста с ингредиентами
folium.LatLngPopup().add_to(m)
folium.Marker([43.1589, 77.0286], popup=f"Ingredients: {ingredients}").add_to(m)

m.save("249.html")