python
        # Import necessary libraries
        import folium

        # Define coordinates of the sources of rivers Ulken Almaty and Urzhar
        ulken_almaty = [43.2508, 76.9197]  # Latitude, Longitude
        urchar = [43.2167, 76.9667]  # Latitude, Longitude

        # Create a map centered around Almaty
        m = folium.Map(location=[43.2508, 76.9197], zoom_start=12)

        # Add markers for the sources of rivers Ulken Almaty and Urzhar
        folium.Marker(ulken_almaty, popup='Исток реки Улькен Алматы').add_to(m)
        folium.Marker(urchar, popup='Исток реки Уржар').add_to(m)

        # Save the map as "99.html"
        m.save("99.html")