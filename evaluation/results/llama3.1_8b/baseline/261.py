import folium

# Создание карты
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)

# Слой с данными о качестве воды в реке Киши Осек
water_quality_data = {
    'location': [55.7558, 37.6173],
    'quality': 'низкое'
}
folium.Marker(location=water_quality_data['location'], popup='Качество воды: '+ water_quality_data['quality']).add_to(m)

# Слой с данными о типах и количестве овощей
vegetable_data = {
    'location': [55.7558, 37.6173],
    'types': ['картофель', 'капуста'],
    'quantity': 1000
}
folium.Marker(location=vegetable_data['location'], popup='Типы овощей: '+ ', '.join(vegetable_data['types']) + ', Количество: ' + str(vegetable_data['quantity'])).add_to(m)

# Объединение слоев данных о качестве воды и типах овощей
folium.Marker(location=[55.7558, 37.6173], popup='Потенциальные риски для здоровья человека: высокие').add_to(m)

# Слой с рекомендациями по безопасному производству засолки овощей
recommendations = {
    'location': [55.7558, 37.6173],
    'recommendations': ['Использовать фильтры для очистки воды', 'Следить за температурой и влажностью']
}
folium.Marker(location=recommendations['location'], popup='Рекомендации: '+ ', '.join(recommendations['recommendations'])).add_to(m)

# Сохранение карты в файл
m.save("261.html")