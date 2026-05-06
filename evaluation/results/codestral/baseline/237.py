python
        import folium

        # Coordinates for the key locations along River Aksu
        source = [41.805, 76.94]  # Source of River Aksu
        junction = [42.35, 76.96]  # Junction with another river or lake
        serving_location = [42.27, 77.18]  # Location where the cocktail is served

        # Create a map centered around the source of River Aksu
        m = folium.Map(location=source, zoom_start=9)

        # Add markers for each key location
        folium.Marker(source, popup='Source of River Aksu').add_to(m)
        folium.Marker(junction, popup='Junction with another river or lake').add_to(m)
        folium.Marker(serving_location, popup='Location where the cocktail is served').add_to(m)

        # Add lines representing the path of the cocktail
        folium.PolyLine([source, junction, serving_location], color="red", weight=2.5, opacity=1).add_to(m)

        # Save the map to an HTML file
        m.save("237.html")