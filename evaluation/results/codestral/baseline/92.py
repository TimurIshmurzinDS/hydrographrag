python
         import geopandas as gpd
         import folium
         from shapely.geometry import Point, LineString

         # Load the rivers data
         rivers = gpd.read_file('rivers_data.shp')  # replace with your file path

         # Define the points of interest
         dos_mouth = Point(37.618423, 55.751244)  # coordinates for the mouth of the Dos River
         emel_start = Point(39.012717, 51.672044)  # coordinates for the start of the Emel River

         # Calculate the distance between the points
         distance = dos_mouth.distance(emel_start)
         print(f'The distance between the mouth of Dos and the start of Emel is: {distance} kilometers')

         # Create a map centered around the points of interest
         m = folium.Map(location=[53, 40], zoom_start=6)

         # Add markers for the points of interest
         folium.Marker([dos_mouth.y, dos_mouth.x], popup='Mouth of Dos').add_to(m)
         folium.Marker([emel_start.y, emel_start.x], popup='Start of Emel').add_to(m)

         # Add a line between the points of interest
         folium.PolyLine([(dos_mouth.y, dos_mouth.x), (emel_start.y, emel_start.x)]).add_to(m)

         # Save the map to an HTML file
         m.save("92.html")