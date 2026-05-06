python
         from geopy.geocoders import Nominatim
         from geopy.distance import distance
         import folium
         # Initialize the geolocator
         geolocator = Nominatim(user_agent="geoapiExercises")
         # Get the coordinates of Karatal and Ulken rivers in Almaty
         karatal_location = geolocator.geocode("Karatal River, Almaty")
         ulken_location = geolocator.geocode("Ulken River, Almaty")
         # Extract the coordinates
         karatal_coordinates = (karatal_location.latitude, karatal_location.longitude)
         ulken_coordinates = (ulken_location.latitude, ulken_location.longitude)
         # Calculate the distance between two points
         dist = distance(karatal_coordinates, ulken_coordinates).kilometers
         print("The distance between Karatal and Ulken rivers is:", round(dist, 2), "km")
         # Visualize the points on a map
         m = folium.Map(location=[(karatal_coordinates[0] + ulken_coordinates[0]) / 2, (karatal_coordinates[1] + ulken_coordinates[1]) / 2], zoom_start=13)
         folium.Marker(karatal_coordinates, popup='Karatal River').add_to(m)
         folium.Marker(ulken_coordinates, popup='Ulken River').add_to(m)
         m.save("102.html")