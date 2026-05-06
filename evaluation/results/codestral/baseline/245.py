python
         import folium
         from pyproj import Geod

         # Define the length of the Kara River in meters (you can get this value using GIS tools)
         kara_river_length = 2000000  # meters

         # Define a constant that represents the relationship between black hole mass and river length
         # This value is hypothetical and should be replaced with a real scientific value or model
         CONSTANT = 1e-6  # meters to solar masses conversion factor

         # Calculate the estimated mass of the black hole
         black_hole_mass = kara_river_length * CONSTANT

         print(f"The estimated mass of the black hole is {black_hole_mass} solar masses.")

         # Define the coordinates of the Kara River (you can get these values using GIS tools)
         river_coordinates = [(69.0128, 74.4531), (69.0128, 74.4532)]  # Example coordinates

         # Create a map centered around the Kara River
         m = folium.Map(location=river_coordinates[0], zoom_start=6)

         # Add a marker to the map at the start of the river
         folium.Marker(river_coordinates[0], popup="Start of the Kara River").add_to(m)

         # Add a line to the map representing the Kara River
         folium.PolyLine(river_coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

         # Save the map as an HTML file
         m.save("245.html")