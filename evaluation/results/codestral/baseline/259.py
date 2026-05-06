python
         import folium
         from geopy.distance import great_circle
         # Define the coordinates of Baskan River and spacecraft
         baskan_river = (43.5806, 41.7294)
         spacecraft = (43.6000, 41.7000)
         # Create a map centered around the Baskan River
         m = folium.Map(location=baskan_river, zoom_start=10)
         # Add markers for Baskan River and spacecraft on the map
         folium.Marker(baskan_river, popup='Baskan River').add_to(m)
         folium.Marker(spacecraft, popup='Spacecraft', icon=folium.Icon(color='red')).add_to(m)
         # Calculate the distance between Baskan River and spacecraft
         distance = great_circle(baskan_river, spacecraft).kilometers
         print(f'Distance between Baskan River and spacecraft: {distance} km')
         # Assume that water availability and infrastructure are checked manually or using additional data sources
         # If water is available and infrastructure exists, then it can be used for engine cooling
         if distance < 100:  # Arbitrary threshold for demonstration purposes
             print('The spacecraft can use water from Baskan River for engine cooling.')
         else:
             print('The spacecraft cannot use water from Baskan River for engine cooling due to the distance.')
         # Save the map as HTML file
         m.save("259.html")