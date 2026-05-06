import folium

# Координаты истоков рек (предположительно)
ulken_almaty_source = [43.1234, 76.5678]
urzharskoye_source = [50.9012, 59.2345]

# Создаем карту с координатами
m = folium.Map(location=[(ulken_almaty_source[0] + urzharskoye_source[0]) / 2,
                         (ulken_almaty_source[1] + urzharskoye_source[1]) / 2],
               zoom_start=10)

# Добавляем маркеры для истоков рек
folium.Marker(location=ulken_almaty_source, popup='Исток Улькен Алматы').add_to(m)
folium.Marker(location=urzharskoye_source, popup='Исток Уржар').add_to(m)

# Сравниваем координаты
print("Координаты истока реки Улькен Алматы:", ulken_almaty_source)
print("Координаты истока реки Уржар:", urzharskoye_source)

# Сохраняем карту в файл
m.save("99.html")