import folium

# Данные о воде из реки Киши Осек (необходимы для моделирования)
water_data = {
    'salinity': 0.5, # %
    'pH': 6.5,
    'contaminants': 'unknown',
}

# Функция расчета пропорций соли
def calculate_salt(weight_vegetables):
  return weight_vegetables * 0.1 # %

# Пример использования функции
weight_vegetables = 1000 # граммы

amount_salt = calculate_salt(weight_vegetables)

print('Количество соли:', amount_salt, 'gram')

# Визуализация на карте (необходима информация о местоположении реки Киши Осек)
m = folium.Map(location=[43.15, 26.05], zoom_start=12) # Примерные координаты

folium.Marker(location=[43.15, 26.05], popup='Река Киши Осек').add_to(m)
m.save("261.html")