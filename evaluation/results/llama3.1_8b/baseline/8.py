import folium

# Загрузите данные о местоположении и состоянии датчика мониторинга
data = {
    'location': [43.1234, 76.5678],  # Координаты реки Улкен Алматы
    'state': 'good'  # Состояние датчика мониторинга (хорошее или плохое)
}

# Создайте слой географических данных для отображения реки Улкен Алматы
m = folium.Map(location=data['location'], zoom_start=12)

# Добавьте маркер на карте, указывающий на местоположение датчика мониторинга
folium.Marker(data['location'], popup='Состояние датчика: ' + data['state']).add_to(m)

# Отобразите состояние датчика мониторинга в виде легенды или всплывающей подсказки
legend = folium.FeatureGroup(name='Состояние датчика')
folium.Marker(data['location'], popup=data['state']).add_to(legend)
legend.add_to(m)

# Сохраните карту как HTML-файл
m.save("8.html")