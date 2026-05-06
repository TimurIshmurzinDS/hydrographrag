python
         import folium
         from folium.plugins import MarkerCluster
         # Define the coordinates of the river Basakan and the point of use
         basakan_river = [54.9836, 72.0167]
         point_of_use = [54.9736, 72.0267]
         # Create a map centered around the river Basakan
         m = folium.Map(location=basakan_river, zoom_start=12)
         # Add markers for the river Basakan and the point of use
         folium.Marker(basakan_river, popup='Река Баскан').add_to(m)
         folium.Marker(point_of_use, popup='Место использования льда').add_to(m)
         # Create a line between the river Basakan and the point of use to represent the ice collection route
         folium.PolyLine([basakan_river, point_of_use], color="red").add_to(m)
         # Save the map as an HTML file
         m.save("267.html")