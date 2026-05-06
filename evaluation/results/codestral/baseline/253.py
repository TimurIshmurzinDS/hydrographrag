python
         from geopy.distance import great_circle
         import folium
         # Координаты Альфы Центавра и реки Караой
         alpha_centauri = (49.18, 67.75)
         karaoy_river = (50.23, 68.87)
         # Расчет расстояния
         distance = great_circle(alpha_centauri, karaoy_river).kilometers
         print(f"Расстояние до Альфы Центавра от реки Караой: {distance} км")
         # Визуализация на карте
         m = folium.Map(location=[50, 68], zoom_start=4)
         folium.Marker(alpha_centauri, popup='Альфа Центавра').add_to(m)
         folium.Marker(karaoy_river, popup='Река Караой').add_to(m)
         line = folium.PolyLine(locations=[alpha_centauri, karaoy_river], weight=2, color='blue')
         m.add_child(line)
         m.save("253.html")