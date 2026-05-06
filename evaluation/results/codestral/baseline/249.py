python
        import math
        import folium
        from geopy.distance import great_circle

        # Coordinates of Talgar River and Jupiter (in decimal degrees)
        talgar_river = (43.75, 71.2833)
        jupiter = (0.0, 51.95)

        # Calculate the distance between Talgar River and Jupiter
        distance = great_circle(talgar_river, jupiter).kilometers

        # Define a list of ingredients based on the distance
        ingredients = {
            "Vodka": 30 + int(distance / 1000),
            "Orange Juice": 60 - int(distance / 1000),
            "Lime Juice": 20,
            "Sugar Syrup": math.sqrt(distance) if distance > 5000 else 0
        }

        # Print the cocktail recipe
        print("Cocktail Recipe:")
        for ingredient, amount in ingredients.items():
            print(f"{ingredient}: {amount} ml")

        # Visualize on a map using folium
        m = folium.Map(location=[40, 30], zoom_start=2)
        folium.Marker(talgar_river, popup="Talgar River").add_to(m)
        folium.Marker(jupiter, popup="Jupiter").add_to(m)
        m.save("249.html")