import folium

# Параметры ирригации для Aksu River
area_aksu = 10000  # площадь полей в гектарах
required_moisture_aksu = 50  # требуемая влажность почвы (мм/день)
efficiency_aksu = 0.8  # коэффициент увлажнения

# Параметры ирригации для Kurty River
area_kurty = 12000  # площадь полей в гектарах
required_moisture_kurty = 55  # требуемая влажность почвы (мм/день)
efficiency_kurty = 0.85  # коэффициент увлажнения

# Текущий дебит рек
discharge_aksu = 100  # дебит Aksu River в м³/с
discharge_kurty = 120  # дебит Kurty River в м³/с

# Расчет потребности в воде на полях для Aksu River
water_needed_aksu = (area_aksu * required_moisture_aksu * efficiency_aksu) / 1000  # в кубических метрах в день

# Расчет потребности в воде на полях для Kurty River
water_needed_kurty = (area_kurty * required_moisture_kurty * efficiency_kurty) / 1000  # в кубических метрах в день

# Сравнение потребности в воде с текущим дебитом рек
irrigation_potential_aksu = discharge_aksu >= water_needed_aksu
irrigation_potential_kurty = discharge_kurty >= water_needed_kurty

# Создание карты для визуализации
m = folium.Map(location=[42.0, 75.0], zoom_start=6)

# Добавление маркеров с информацией о ирригационном потенциале
folium.Marker(
    location=[42.0, 75.0],
    popup=f"Aksu River: {'Ирригационный потенциал' if irrigation_potential_aksu else 'Недостаточный дебит'}",
    icon=folium.Icon(color='green' if irrigation_potential_aksu else 'red')
).add_to(m)

folium.Marker(
    location=[42.0, 75.1],
    popup=f"Kurty River: {'Ирригационный потенциал' if irrigation_potential_kurty else 'Недостаточный дебит'}",
    icon=folium.Icon(color='green' if irrigation_potential_kurty else 'red')
).add_to(m)

# Сохранение карты
m.save("114.html")